from PyQt5.QtCore import pyqtSignal, QObject

class SignalEmitter(QObject):
    sync_data_created = pyqtSignal(object)
    timeout_interval_changed = pyqtSignal(int)
    online_status_updated = pyqtSignal(bool)

    def __init__(self):
        super().__init__()