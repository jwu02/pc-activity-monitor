from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtCore import Qt

import time
from datetime import datetime

class ActivitySummary(QWidget):
    def __init__(self):
        super().__init__()

        self.application_launch_time = time.time()
        
        self.data = {
            'activities': {
                'key-presses': [],
                'left-clicks': [],
                'right-clicks': [],
                'mouse-movements': []
            },
            'timestamps': []
        }

        self.initUI()

    def initUI(self):
        self.layout = QGridLayout(self)
        
        time_formatted = datetime.fromtimestamp(self.application_launch_time).strftime("%Y-%m-%d %H:%M:%S")
        self.layout.addWidget(QLabel(f"Recording activity since {time_formatted}"), 0, 0, 1, 4)

        self.summary_labels = {}
        self.data_text_labels = {
            'key-presses': 'Key Presses',
            'left-clicks': 'Left Clicks',
            'right-clicks': 'Right Clicks',
            'mouse-movements': 'Mouse Movements'
        }

        # Add data labels and the corresponding summary/sum under it
        for i, (k, v) in enumerate(self.data['activities'].items()):
            self.layout.addWidget(QLabel(self.data_text_labels[k]), 1, i, alignment=Qt.AlignCenter)

            # store reference so we can update it later
            self.summary_labels[k] = QLabel(self.format_summary_text(k, sum(v)))
            self.summary_labels[k].setStyleSheet("font-weight: 900; font-size: 24px;")
            self.layout.addWidget(self.summary_labels[k], 2, i, alignment=Qt.AlignCenter)
    
    def set_data(self, data):
        self.data = data
        # update data summary labels
        for k, v in self.data['activities'].items():
            self.summary_labels[k].setText(self.format_summary_text(k, sum(v)))
            

    def format_summary_text(self, key, total_value):
        output_str = ''
        if key=='mouse-movements':
            output_str = str(round(total_value, 1)) + ' m'
        else:
            output_str = str(total_value)
        
        return output_str