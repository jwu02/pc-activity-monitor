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

from view.logger_widget import LoggerWidget
from view.activity_plot_widget import ActivityPlotWidget
from view.activity_summary import ActivitySummary

from workers.worker import Worker

load_dotenv()  # This will load variables from the .env file into environment variables
API_ENDPOINT = os.getenv('API_ENDPOINT')
API_BEARER_TOKEN = os.getenv('API_STATIC_TOKEN')


class ActivityDashboard(QWidget):
    def __init__(self, side_panel_widget):
        super().__init__()

        self.timeout_interval_slider = side_panel_widget.timeout_interval_slider
        self.timeout_interval_slider.timeoutIntervalChanged.connect(self.update_timeout_interval)
        self.timeout_interval = 60000 # Interval at which to send data in minutes

        self.online_status_label = side_panel_widget.online_status_label
        self.online = self.online_status_label.online
        self.online_status_label.online_status_updated.connect(self.update_online_status)

        self.key_presses = []
        self.left_clicks = []
        self.right_clicks = []
        self.mouse_movements = []
        self.timestamps = []

        self.init_mnk_listener()
        self.initUI()

        self.threadpool = QThreadPool()
        # print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

    def init_mnk_listener(self):
        # Global variables to count key presses, mouse clicks, and track mouse movement
        self.left_click_count = 0
        self.right_click_count = 0
        self.key_press_count = 0
        self.total_mouse_distance_pixels = 0
        self.dpi_x = 96  # Default DPI value, adjust if needed
        self.last_mouse_pos = None
        self.total_mouse_distance_meters = 0

        # Start listening to mouse and keyboard events
        self.mouse_listener = mouse.Listener(on_click=self.on_click, on_move=self.on_move)
        self.mouse_listener.start()
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.keyboard_listener.start()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.send_data_timer = QTimer(self)
        self.send_data_timer.setInterval(self.timeout_interval)
        self.send_data_timer.timeout.connect(self.post_data_worker)
        self.send_data_timer.start()

        self.update_remaining_time_timer = QTimer(self)
        self.update_remaining_time_timer.setInterval(1000)
        self.update_remaining_time_timer.timeout.connect(self.update_remaining_time_label)
        self.update_remaining_time_timer.start()

        self.activity_summary = ActivitySummary()
        self.activity_plot = ActivityPlotWidget()
        self.remaining_time_prefix = "Remaining time until next POST request: "
        self.remaining_time_label = QLabel(self.get_remaining_time_label_text())
        self.log_text_box = LoggerWidget()

        self.layout.addWidget(self.activity_summary)
        self.layout.addWidget(self.activity_plot)
        self.layout.addWidget(self.remaining_time_label)
        self.layout.addWidget(self.log_text_box)

    def on_click(self, x, y, button, pressed):
        if pressed:
            if button == mouse.Button.left:
                self.left_click_count += 1
            elif button == mouse.Button.right:
                self.right_click_count += 1

    def on_move(self, x, y):
        if self.last_mouse_pos is not None:
            # Calculate distance moved in pixels
            dx = x - self.last_mouse_pos[0]
            dy = y - self.last_mouse_pos[1]
            distance_pixels = math.sqrt(dx * dx + dy * dy)
            
            # Accumulate total distance in pixels
            self.total_mouse_distance_pixels += distance_pixels
            
            # Convert accumulated distance to meters
            self.total_mouse_distance_meters = (self.total_mouse_distance_pixels / self.dpi_x) * 0.0254
        
        # Update last position
        self.last_mouse_pos = (x, y)

    def on_press(self, key):
        self.key_press_count += 1

    def process_data(self, progress_callback):
        if self.online:
            self.post_data(progress_callback)
        else:
            progress_callback.emit("Currently offline. Queuing data for syncing later.")

    def post_data(self, progress_callback):
        HEADERS = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_BEARER_TOKEN}'
        }
        
        if not (self.key_press_count==0 and self.left_click_count==0 and 
                self.right_click_count==0 and self.total_mouse_distance_pixels==0):
            try:
                progress_callback.emit("Starting data send cycle...")

                timestamp = datetime.now(timezone.utc).isoformat()  # ISO 8601 format with UTC timezone

                dataObj = {
                    'key-presses': {'count': self.key_press_count, 'createdAt': timestamp},
                    'left-clicks': {'count': self.left_click_count, 'createdAt': timestamp},
                    'right-clicks': {'count': self.right_click_count, 'createdAt': timestamp},
                    'mouse-movements': {'amount': self.total_mouse_distance_meters, 'createdAt': timestamp}
                }

                for key, val in dataObj.items():
                    POST_REQUEST_ENDPOINT = f'{API_ENDPOINT}/{key}'
                    progress_callback.emit(f"POST {POST_REQUEST_ENDPOINT}")
                    requests.post(POST_REQUEST_ENDPOINT, data=json.dumps(dataObj[key]), headers=HEADERS)

            except requests.exceptions.RequestException as e:
                print(f"Error sending data: {e}")

            progress_callback.emit("Data sent successfully.")
        else:
            progress_callback.emit("No activity recorded.")
    
    def post_data_worker(self):
        # Pass the function to execute
        worker = Worker(self.process_data) # Any other args, kwargs are passed to the run function
        # worker.signals.result.connect(self.print_output)
        worker.signals.progress.connect(self.log_text_box.logMessage)
        worker.signals.finished.connect(self.post_cycle_complete)

        # Execute
        self.threadpool.start(worker)

    def post_cycle_complete(self):
        self.update_recorded_data()
        self.reset_count()
    
    def update_recorded_data(self):
        # record data in widget
        self.key_presses.append(self.key_press_count)
        self.left_clicks.append(self.left_click_count)
        self.right_clicks.append(self.right_click_count)
        self.mouse_movements.append(self.total_mouse_distance_meters)
        self.timestamps.append(time.time())

        # update plot widget with new date
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
    
    def update_timeout_interval(self, value: int):
        self.timeout_interval = value*60000
        self.send_data_timer.setInterval(self.timeout_interval)

    def update_remaining_time_label(self):
        self.remaining_time_label.setText(self.get_remaining_time_label_text())
    
    def get_remaining_time_label_text(self) -> str:
        remaining_time = self.send_data_timer.remainingTime()

        remaining_time_formatted = self.milliseconds_to_mmss(remaining_time)
    
        return f"Time remaining until next POST request: {remaining_time_formatted}"

    def milliseconds_to_mmss(self, milliseconds: int):
        seconds = (milliseconds // 1000) % 60
        minutes = (milliseconds // (1000 * 60)) % 60
        return f"{int(minutes):02}:{int(seconds):02}"

    def update_online_status(self, online: bool):
        self.online = online
        self.log_text_box.logMessage(f"You are now {"ONLINE" if self.online else "OFFLINE"}.")