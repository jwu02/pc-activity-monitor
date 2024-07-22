from datetime import datetime
import queue

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel
from PyQt5.QtGui import QTextCursor

import qtawesome as qta

class DataSyncWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.sync_data_created_signal = None

        self.sync_data_queue = queue.Queue()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Sync Offline Data")
        
        layout = QVBoxLayout()
        self.requests_label = QTextEdit("")
        self.requests_label.setReadOnly(True)

        layout.addWidget(self.requests_label)
        
        self.setLayout(layout)
    
    def set_sync_data_created_signal(self, signal):
        self.sync_data_created_signal = signal
        self.sync_data_created_signal.connect(self.add_sync_data_point)
    
    def add_sync_data_point(self, new_data_point):
        self.sync_data_queue.put(new_data_point)
        self.update_ui(new_data_point)
    
    def update_ui(self, dp):
        # https://stackoverflow.com/questions/5466451/how-do-i-escape-curly-brace-characters-in-a-string-while-using-format-or
        output = f"""{{
    Key Presses: {dp['key-presses']['count']},
    Left Clicks: {dp['left-clicks']['count']},
    Right Clicks: {dp['right-clicks']['count']},
    Mouse Movements: {dp['mouse-movements']['amount']}
}} @ {datetime.fromisoformat(dp['key-presses']['createdAt']).strftime('%Y-%m-%d %H:%M:%S')}\n
"""
        
        self.requests_label.append(output)
        self.requests_label.moveCursor(QTextCursor.End)