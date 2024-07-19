from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt

from view.timeout_interval_slider_widget import TimeoutIntervalSliderWidget
from view.online_status_label import OnlineStatusLabel

class SidePanelWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
    
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        self.online_status_label = OnlineStatusLabel()
        self.timeout_interval_slider = TimeoutIntervalSliderWidget()

        self.layout.addWidget(self.online_status_label)
        self.layout.addWidget(self.timeout_interval_slider)
        