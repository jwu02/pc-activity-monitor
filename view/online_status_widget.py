from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy, QPushButton
from PyQt5.QtCore import Qt, QThreadPool
import qtawesome as qta

from dotenv import load_dotenv
import os
import requests

from workers.worker import Worker

load_dotenv() # This will load variables from the .env file into environment variables
API_ENDPOINT = os.getenv('API_ENDPOINT')
API_BEARER_TOKEN = os.getenv('API_STATIC_TOKEN')

class OnlineStatusWidget(QWidget):

    STATUS_MAPPING = {
        True: {
            "label": "Online",
            "tooltip": "Go Offline",
            "color": "green"
        },
        False: {
            "label": "Offline",
            "tooltip": "Go Online",
            "color": "grey"
        }
    }

    def __init__(self, online_status_updated_signal):
        super().__init__()

        self.is_online = False
    
        self.initUI()

        self.threadpool = QThreadPool()

        self.online_status_updated_signal = online_status_updated_signal
        self.online_status_updated_signal.connect(self.updateUI)
        self.toggle_online_status() # go online on initialization

    def initUI(self):
        self.layout = QHBoxLayout(self)

        self.status_label = QLabel(self.STATUS_MAPPING[self.is_online]["label"], self)
        self.update_status_label_stylesheet()
        # Set the alignment of the text within the QLabel to center
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.status_label.adjustSize()

        # Toggle online / offline btn
        self.connect_icon = qta.icon('fa5s.plug')
        self.disconnect_icon = qta.icon('mdi6.connection')

        self.toggle_status_btn = QPushButton(self.connect_icon, None)
        self.toggle_status_btn.clicked.connect(self.toggle_online_status)
        self.toggle_status_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.toggle_status_btn.adjustSize()

        # map the online status to the toggle status button tooltip description
        toggle_btn_tooltip = self.STATUS_MAPPING[self.is_online]["tooltip"]
        self.toggle_status_btn.setToolTip(toggle_btn_tooltip)

        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.toggle_status_btn)

    def update_status_label_stylesheet(self):
        self.status_label_stylesheet = f"""
            color: white;
            background-color: {self.STATUS_MAPPING[self.is_online]["color"]};
            padding: 4px 10px;
            text-align: center;
            font-weight: bold;
        """
        self.status_label.setStyleSheet(self.status_label_stylesheet)

    def toggle_online_status(self):
        # if status is toggled to online, check server connection
        if not self.is_online:
            self.ping_worker()
        else:
            self.is_online = False
        
        self.updateUI()
        self.online_status_updated_signal.emit(self.is_online)

    def updateUI(self):
        self.toggle_status_btn.setIcon(self.disconnect_icon if self.is_online else self.connect_icon)
        self.status_label.setText(self.STATUS_MAPPING[self.is_online]["label"])
        
        tooltip = self.STATUS_MAPPING[self.is_online]["tooltip"]
        self.toggle_status_btn.setToolTip(tooltip)

        self.update_status_label_stylesheet()
    
    def ping_worker(self):
        self.toggle_status_btn.setEnabled(False)

        # Pass the function to execute
        worker = Worker(self.ping_api_server) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.set_online_status)
        worker.signals.progress.connect(print)
        worker.signals.finished.connect(self.enable_toggle_btn)

        # Execute
        self.threadpool.start(worker)

    def enable_toggle_btn(self):
        self.toggle_status_btn.setEnabled(True)

    def ping_api_server(self, progress_callback):
        try:
            response = requests.get(f'{API_ENDPOINT}/ping')
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.RequestException as e:
            print(f"Error pinging server: {e}")
            return False
    
    def set_online_status(self, is_online):
        self.is_online = is_online

        self.updateUI()
        self.online_status_updated_signal.emit(self.is_online)