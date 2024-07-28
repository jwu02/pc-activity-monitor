from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt

from view.side_panel.timeout_interval_slider_widget import TimeoutIntervalSliderWidget
from view.side_panel.online_status_widget import OnlineStatusWidget
from view.side_panel.data_sync_widget import DataSyncWindow

class SidePanelWidget(QWidget):
    def __init__(self, signal_emitter):
        super().__init__()

        self.signal_emitter = signal_emitter

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        self.online_status_widget = OnlineStatusWidget(self.signal_emitter)
        self.timeout_interval_slider = TimeoutIntervalSliderWidget(self.signal_emitter.timeout_interval_changed)

        self.data_sync_window = DataSyncWindow(self.signal_emitter)
        self.sync_data_btn = QPushButton("Sync Offline Data")
        self.sync_data_btn.clicked.connect(self.data_sync_window.show)

        self.layout.addWidget(self.online_status_widget)
        self.layout.addWidget(self.timeout_interval_slider)
        self.layout.addWidget(self.sync_data_btn)
