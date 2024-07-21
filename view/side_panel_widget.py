from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt

from view.timeout_interval_slider_widget import TimeoutIntervalSliderWidget
from view.online_status_widget import OnlineStatusWidget
from view.data_sync_widget import DataSyncWindow

class SidePanelWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
    
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        self.online_status_widget = OnlineStatusWidget()
        self.timeout_interval_slider = TimeoutIntervalSliderWidget()

        self.data_sync_window = DataSyncWindow()
        self.sync_data_btn = QPushButton("Sync Offline Data")
        self.sync_data_btn.clicked.connect(self.show_sync_data_window)

        self.layout.addWidget(self.online_status_widget)
        self.layout.addWidget(self.timeout_interval_slider)
        self.layout.addWidget(self.sync_data_btn)
    
    def show_sync_data_window(self):
        self.data_sync_window.show()

    def set_sync_data_created_signal(self, signal):
        self.data_sync_window.set_sync_data_created_signal(signal)