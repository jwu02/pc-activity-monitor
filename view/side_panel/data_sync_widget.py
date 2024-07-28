from datetime import datetime
import queue

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt

import qtawesome as qta

class DataSyncWindow(QWidget):
    def __init__(self, signal_emitter):
        super().__init__()

        self.signal_emitter = signal_emitter

        self.is_online = False
        self.signal_emitter.online_status_updated.connect(self.set_online_status)

        self.sync_data_created_signal = self.signal_emitter.sync_data_created
        self.sync_data_created_signal.connect(self.add_sync_data_point)

        self.sync_data_queue = queue.Queue()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Sync Offline Data")

        sync_icon = qta.icon('fa5s.sync-alt')
        erase_icon = qta.icon('fa5s.eraser')
        
        layout = QVBoxLayout()

        btn_group_layout = QHBoxLayout()
        sync_offline_data_btn = QPushButton(sync_icon, "Sync All")
        sync_offline_data_btn.clicked.connect(self.sync_all_offline_data)

        clear_offline_data_btn = QPushButton(erase_icon, "Clear All")
        clear_offline_data_btn.clicked.connect(self.clear_all_offline_data)

        self.offline_data_table = QTableWidget()
        self.offline_data_table.setColumnCount(5)
        self.offline_data_table.verticalHeader().setVisible(False) # hides table row indicies
        self.offline_data_table.setHorizontalHeaderLabels(['Key Presses', 'Left Clicks', 'Right Clicks', 'Mouse Movements', 'Timestamp'])
        # Disable selection
        self.offline_data_table.setSelectionBehavior(QTableWidget.SelectItems)
        self.offline_data_table.setSelectionMode(QTableWidget.NoSelection)
        self.offline_data_table.setEditTriggers(QTableWidget.NoEditTriggers)

        btn_group_layout.addWidget(sync_offline_data_btn)
        btn_group_layout.addWidget(clear_offline_data_btn)
        
        layout.addLayout(btn_group_layout)
        layout.addWidget(self.offline_data_table)
        self.setLayout(layout)
    
    def set_online_status(self, is_online):
        self.is_online = is_online

    def add_sync_data_point(self, new_data_point):
        self.sync_data_queue.put(new_data_point)
        self.update_ui()
    
    def update_ui(self):
        temp_data = list(self.sync_data_queue.queue)

        self.offline_data_table.setRowCount(len(temp_data))

        for row, data_obj in enumerate(temp_data):
        
            timestamp = data_obj.get('key-presses', {}).get('createdAt', '')

            for col, (key, val_obj) in enumerate(data_obj.items()):
                val = round(val_obj['amount'], 2) if key=='mouse-movements' else val_obj['count']
                cell = QTableWidgetItem(str(val))
                cell.setFlags(cell.flags() ^ Qt.ItemIsEditable) # Set cell values to read-only
            
                self.offline_data_table.setItem(row, col, cell)

            # Parse the ISO 8601 string into a datetime object with timezone info
            utc_dt = datetime.fromisoformat(timestamp)
            local_dt = utc_dt.astimezone() # Convert from UTC to local time

            # Format the datetime object as needed
            formatted_local_time = local_dt.strftime('%Y-%m-%d %H:%M:%S')

            self.offline_data_table.setItem(row, 4, QTableWidgetItem(formatted_local_time))

        self.offline_data_table.scrollToBottom()

    def sync_all_offline_data(self):
        while not self.sync_data_queue.empty():
            if self.is_online:
                data = self.sync_data_queue.get()
                self.signal_emitter.send_sync_data.emit(data)
            else:
                break
        
        self.update_ui()

    def clear_all_offline_data(self):
        self.sync_data_queue = queue.Queue()
        self.offline_data_table.setRowCount(0)