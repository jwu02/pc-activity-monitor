from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QSystemTrayIcon, QMenu
from PyQt6.QtCore import QCoreApplication
from PyQt6.QtGui import QAction

import qtawesome as qta

from view.activity_dashboard.activity_dashboard import ActivityDashboard
from view.side_panel.side_panel_widget import SidePanelWidget
from view.signal_emitter import SignalEmitter

class MainWindow(QMainWindow):
    signal_emitter = SignalEmitter()

    def __init__(self) -> None:
        super().__init__()

        self.initUI()

    def initUI(self):
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

        # Set up system tray icon
        self.tray_icon = QSystemTrayIcon(qta.icon('fa5s.rocket'), self)

        tray_menu = QMenu() # Create a menu for the tray icon
        
        # Create exit action
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(QCoreApplication.instance().quit)
        tray_menu.addAction(exit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.restore_window)
        self.tray_icon.show()
    
    def closeEvent(self, event):
        # Hide the window when trying to close it
        self.hide()
        self.tray_icon.showMessage(
            'Application minimized',
            'The application has been minimized to the system tray.',
            QSystemTrayIcon.Information,
            2000
        )
        event.ignore()

    def restore_window(self, reason):
        # Restore the window when the tray icon is clicked
        if reason == QSystemTrayIcon.ActivationReason.Trigger:  # Clicked by left mouse button
            self.show()
            self.raise_()  # Bring the window to the front