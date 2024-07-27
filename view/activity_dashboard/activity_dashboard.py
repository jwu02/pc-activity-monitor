from datetime import datetime, timezone
from dotenv import load_dotenv
import json
import math
import os
from pynput import mouse, keyboard
import requests
import time

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QThreadPool, QTimer
from PyQt5.QtGui import QGuiApplication

from view.activity_dashboard.logger_widget import LoggerWidget
from view.activity_dashboard.activity_plot_widget import ActivityPlotWidget
from view.activity_dashboard.activity_summary import ActivitySummary

from workers.worker import Worker

load_dotenv()  # This will load variables from the .env file into environment variables
API_ENDPOINT = os.getenv('API_ENDPOINT')
API_BEARER_TOKEN = os.getenv('API_STATIC_TOKEN')


class ActivityDashboard(QWidget):
    def __init__(self, signal_emitter):
        super().__init__()

        self.signal_emitter = signal_emitter

        self.is_online = False
        self.signal_emitter.online_status_updated.connect(self.update_online_status)

        self.timeout_interval = 5000 # Interval at which to send data in minutes
        self.signal_emitter.timeout_interval_changed.connect(self.update_timeout_interval)

        self.signal_emitter.send_sync_data.connect(self.send_data_worker)

        self.log_message_signal = self.signal_emitter.log_message

        self.key_presses = []
        self.left_clicks = []
        self.right_clicks = []
        self.mouse_movements = []
        self.timestamps = []

        self.init_mnk_listener()
        self.initUI()

        self.threadpool = QThreadPool()

    def init_mnk_listener(self):
        # Global variables to count key presses, mouse clicks, and track mouse movement
        self.key_press_count = 0
        self.key_state = {}
        
        self.left_click_count = 0
        self.right_click_count = 0

        self.total_mouse_distance_pixels = 0
        self.screen_dpi = self.get_screen_dpi()
        self.last_mouse_pos = None
        self.total_mouse_distance_meters = 0

        # Start listening to mouse and keyboard events
        self.mouse_listener = mouse.Listener(on_click=self.on_click, on_move=self.on_move)
        self.mouse_listener.start()
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.keyboard_listener.start()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.send_data_timer = QTimer(self)
        self.send_data_timer.setInterval(self.timeout_interval)
        self.send_data_timer.timeout.connect(self.process_data)
        self.send_data_timer.start()

        self.update_remaining_time_timer = QTimer(self)
        self.update_remaining_time_timer.setInterval(1000)
        self.update_remaining_time_timer.timeout.connect(self.update_remaining_time_label)
        self.update_remaining_time_timer.start()

        self.activity_summary = ActivitySummary()
        self.activity_plot = ActivityPlotWidget()
        self.remaining_time_prefix = "Remaining time until next POST request: "
        self.remaining_time_label = QLabel(self.get_remaining_time_label_text())
        self.log_text_box = LoggerWidget(self.signal_emitter)

        self.layout.addWidget(self.activity_summary)
        self.layout.addWidget(self.activity_plot)
        self.layout.addWidget(self.remaining_time_label)
        self.layout.addWidget(self.log_text_box)
    
    def on_press(self, key):
        # Convert key to string for tracking
        try:
            key_char = key.char
        except AttributeError:
            key_char = str(key)  # Handle special keys like '<space>'

        # Initialize key state if not already done
        if key_char not in self.key_state:
            self.key_state[key_char] = True  # Set to True initially for counting the first press

        # Count the key press only if it was previously lifted
        if self.key_state[key_char]:
            self.key_press_count += 1
            self.key_state[key_char] = False  # Mark the key as pressed

    def on_release(self, key):
        try:
            key_char = key.char
        except AttributeError:
            key_char = str(key)

        self.key_state[key_char] = True # Mark the key as lifted

    def on_click(self, x, y, button, pressed):
        if pressed:
            if button == mouse.Button.left:
                self.left_click_count += 1
            elif button == mouse.Button.right:
                self.right_click_count += 1
    
    def get_screen_dpi(self):
        dpi = 120  # Default DPI value

        screen = QGuiApplication.primaryScreen()
        if screen:
            # Retrieve DPI values
            dpi = screen.physicalDotsPerInch()
            print(f"Screen DPI: {dpi}")
        else:
            print(f"Unable to get screen DPI. Setting {dpi} as the default value.")

        return dpi

    def on_move(self, x, y):
        if self.last_mouse_pos is not None:
            # Calculate distance moved in pixels
            dx = x - self.last_mouse_pos[0]
            dy = y - self.last_mouse_pos[1]
            distance_pixels = math.sqrt(dx * dx + dy * dy)
            
            # Accumulate total distance in pixels
            self.total_mouse_distance_pixels += distance_pixels
            
            # Convert accumulated distance to meters
            self.total_mouse_distance_meters = (self.total_mouse_distance_pixels / self.screen_dpi) * 0.0254
        
        # Update last position
        self.last_mouse_pos = (x, y)
    
    def process_data(self):
        """
        The entry point for when the interval timer is up
        """
        if not (self.key_press_count==0 and self.left_click_count==0 and 
                self.right_click_count==0 and self.total_mouse_distance_pixels==0):

            timestamp = datetime.now(timezone.utc).isoformat()  # ISO 8601 format with UTC timezone

            data = {
                'key-presses': {'count': self.key_press_count, 'createdAt': timestamp},
                'left-clicks': {'count': self.left_click_count, 'createdAt': timestamp},
                'right-clicks': {'count': self.right_click_count, 'createdAt': timestamp},
                'mouse-movements': {'amount': self.total_mouse_distance_meters, 'createdAt': timestamp}
            }

            self.send_data_worker(data)
            
        else:
            self.log_message_signal.emit("No activity recorded.")
            self.update_recorded_data()
    
    def send_data_worker(self, data):
        def worker_finished():
            self.update_recorded_data()
            self.reset_count()

        # Check if online first to determine to send or
        # Queue the data for syncing later
        if self.is_online:
            # Pass the function to execute
            # Any other args, kwargs are passed to the run function
            worker = Worker(self.post_data, data)
            
            worker.signals.progress.connect(self.log_message_signal.emit)
            worker.signals.finished.connect(worker_finished)
        else:
            worker = Worker(self.queue_data, data)
            
            worker.signals.progress.connect(self.log_message_signal.emit)
            worker.signals.finished.connect(worker_finished)
        
        self.threadpool.start(worker)
    
    def queue_data(self, data, progress_callback):
        progress_callback.emit("Currently OFFLINE. Queuing data for syncing later.")
        self.signal_emitter.sync_data_created.emit(data)

    def post_data(self, data, progress_callback):
        HEADERS = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_BEARER_TOKEN}'
        }
        
        try:
            progress_callback.emit("Starting data send cycle...")

            for activity_type, activity_data in data.items():
                POST_REQUEST_ENDPOINT = f'{API_ENDPOINT}/activity/{activity_type}'
                progress_callback.emit(f"POST {POST_REQUEST_ENDPOINT}")
                requests.post(POST_REQUEST_ENDPOINT, data=json.dumps(activity_data), headers=HEADERS)

            progress_callback.emit("Data sent successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Error sending data: {e}")
    
    def update_recorded_data(self):
        # Record data in plot widget
        self.key_presses.append(self.key_press_count)
        self.left_clicks.append(self.left_click_count)
        self.right_clicks.append(self.right_click_count)
        self.mouse_movements.append(self.total_mouse_distance_meters)
        self.timestamps.append(time.time())

        # Update plot widget with new date
        updated_data = {
            'activities': {
                'key-presses': self.key_presses,
                'left-clicks': self.left_clicks,
                'right-clicks': self.right_clicks,
                'mouse-movements': self.mouse_movements
            },
            'timestamps': self.timestamps
        }

        self.activity_plot.set_data(updated_data)
        self.activity_summary.set_data(updated_data)

    def reset_count(self) -> None:
        self.key_press_count = 0
        self.left_click_count = 0
        self.right_click_count = 0
        self.total_mouse_distance_pixels = 0
        self.total_mouse_distance_meters = 0
    
    def update_timeout_interval(self, multiplier: int):
        self.timeout_interval = multiplier*60000
        self.send_data_timer.setInterval(self.timeout_interval)

    def update_remaining_time_label(self):
        self.remaining_time_label.setText(self.get_remaining_time_label_text())
    
    def get_remaining_time_label_text(self) -> str:
        remaining_time = self.send_data_timer.remainingTime()

        remaining_time_formatted = milliseconds_to_mmss_format(remaining_time)
    
        return f"Time remaining until next POST request: {remaining_time_formatted}"

    def update_online_status(self, is_online: bool):
        self.is_online = is_online
        self.log_message_signal.emit(f"You are now {'ONLINE' if self.is_online else 'OFFLINE'}.")


def milliseconds_to_mmss_format(milliseconds: int):
    seconds = (milliseconds // 1000) % 60
    minutes = (milliseconds // (1000 * 60)) % 60
    return f"{int(minutes):02}:{int(seconds):02}"