from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QApplication
from PyQt5.QtGui import QFontDatabase, QFont

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


if __name__=="__main__":
    app = QApplication([])

    # Load the Roboto Mono font
    font_id = QFontDatabase.addApplicationFont("fonts/Roboto_Mono/static/RobotoMono-Regular.ttf")
    if font_id == -1:
        print("Failed to load Roboto Mono font.")
    else:
        roboto_mono = QFont("Roboto Mono", 9)
        QApplication.setFont(roboto_mono)  # Set the global font

    mw = MainWindow()

    # Run the app
    app.exec()