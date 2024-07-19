from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal

import qtawesome as qta

class OnlineStatusLabel(QWidget):
    online_status_updated = pyqtSignal(bool)

    STATUS_MAPPING = {
        True: {
            "label": "Online",
            "tooltip": "Go Offline",
            "color": "green"
        },
        False: {
            "label": "Offline",
            "tooltip": "Go Online",
            "color": "grey"
        }
    }

    def __init__(self, parent=None):
        super().__init__(parent)

        self.online = False
    
        self.initUI()
        # go online on initialization
        self.toggle_status()

    def initUI(self):
        self.layout = QHBoxLayout(self)

        self.status_label = QLabel(self.STATUS_MAPPING[self.online]["label"], self)
        self.update_status_label_stylesheet()
        # Set the alignment of the text within the QLabel to center
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.status_label.adjustSize()

        # Toggle online / offline btn
        self.connect_icon = qta.icon('fa5s.plug')
        self.disconnect_icon = qta.icon('mdi6.connection')

        self.toggle_status_btn = QPushButton(self.connect_icon, None)
        self.toggle_status_btn.clicked.connect(self.toggle_status)
        self.toggle_status_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.toggle_status_btn.adjustSize()

        # map the online status to the toggle status button tooltip description
        toggle_btn_tooltip = self.STATUS_MAPPING[self.online]["tooltip"]
        self.toggle_status_btn.setToolTip(toggle_btn_tooltip)

        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.toggle_status_btn)

    def update_status_label_stylesheet(self):
        self.status_label_stylesheet = f"""
            color: white;
            background-color: {self.STATUS_MAPPING[self.online]["color"]};
            padding: 4px 10px;
            text-align: center;
            font-weight: bold;
        """
        self.status_label.setStyleSheet(self.status_label_stylesheet)

    def toggle_status(self):
        self.online = not self.online
        self.updateUI()
        self.online_status_updated.emit(self.online)

    def updateUI(self):
        self.toggle_status_btn.setIcon(self.disconnect_icon if self.online else self.connect_icon)
        self.status_label.setText(self.STATUS_MAPPING[self.online]["label"])
        
        tooltip = self.STATUS_MAPPING[self.online]["tooltip"]
        self.toggle_status_btn.setToolTip(tooltip)

        self.update_status_label_stylesheet()