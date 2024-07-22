from datetime import datetime, timezone
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PyQt5.QtGui import QTextCursor

class LoggerWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create a vertical layout
        layout = QVBoxLayout()

        # Create log display widget
        self.logDisplay = QTextEdit(self)
        self.logDisplay.setReadOnly(True)

        layout.addWidget(self.logDisplay)

        # Set the layout of the widget
        self.setLayout(layout)

    def logMessage(self, message: str):
        self.logDisplay.append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
        # https://stackoverflow.com/questions/7778726/autoscroll-pyqt-qtextwidget
        # TODO only auto scroll to end if already at end
        self.logDisplay.moveCursor(QTextCursor.End)