from PyQt5.QtCore import pyqtSignal, QObject

class SignalEmitter(QObject):
    online_status_updated = pyqtSignal(bool)
    timeout_interval_changed = pyqtSignal(int)
    sync_data_created = pyqtSignal(object)
    send_sync_data = pyqtSignal(object)
    log_message = pyqtSignal(str)

    def __init__(self):
        super().__init__()