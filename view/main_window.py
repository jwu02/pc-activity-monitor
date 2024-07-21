from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout

from view.activity_dashboard import ActivityDashboard
from view.side_panel_widget import SidePanelWidget

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        
        self.setWindowTitle("Activity Monitor")

        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a horizontal layout for the central widget
        horizontal_layout = QHBoxLayout(central_widget)

        # Create two vertical layouts
        side_panel_widget = SidePanelWidget()
        activity_monitor_widget = ActivityDashboard(side_panel_widget)

        # Add the vertical layouts to the horizontal layout
        horizontal_layout.addWidget(side_panel_widget)
        horizontal_layout.addWidget(activity_monitor_widget)

        # self.apply_stylesheet()
        self.show()
    
    def apply_stylesheet(self):
        stylesheet = """
            QLabel, QPushButton, QTextEdit {
                font-size: 16px;
            }
        """

        self.setStyleSheet(stylesheet)