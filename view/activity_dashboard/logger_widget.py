from datetime import datetime, timezone
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PyQt6.QtGui import QTextCursor
from PyQt6.QtCore import Qt

class LoggerWidget(QWidget):
    def __init__(self, signal_emitter):
        super().__init__()

        self.signal_emitter = signal_emitter
        self.signal_emitter.log_message.connect(self.logMessage)

        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()

        # Create log display widget
        self.log_display = QTextEdit(self)
        self.log_display.setReadOnly(True)
        # self.log_display.setLineWrapMode(QTextEdit.NoWrap)
        # self.log_display.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        layout.addWidget(self.log_display)
        self.setLayout(layout)

    def logMessage(self, message: str):
        self.log_display.append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
        # https://stackoverflow.com/questions/7778726/autoscroll-pyqt-qtextwidget
        # TODO only auto scroll to end if already at end
        self.log_display.moveCursor(QTextCursor.End)