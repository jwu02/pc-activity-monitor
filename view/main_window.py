from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PyQt5.QtCore import pyqtSignal

from view.activity_dashboard import ActivityDashboard
from view.side_panel_widget import SidePanelWidget
from view.signal_emitter import SignalEmitter

class MainWindow(QMainWindow):
    signal_emitter = SignalEmitter()

    def __init__(self) -> None:
        super().__init__()
        
        self.setWindowTitle("Activity Monitor")

        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a horizontal layout for the central widget
        horizontal_layout = QHBoxLayout(central_widget)

        # Create two vertical layouts
        side_panel_widget = SidePanelWidget(self.signal_emitter)
        activity_monitor_widget = ActivityDashboard(self.signal_emitter)

        # Add the vertical layouts to the horizontal layout
        horizontal_layout.addWidget(side_panel_widget)
        horizontal_layout.addWidget(activity_monitor_widget)

        self.show()