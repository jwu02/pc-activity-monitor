from datetime import datetime
import queue

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt

import qtawesome as qta

class DataSyncWindow(QWidget):
    def __init__(self, sync_data_created_signal):
        super().__init__()

        self.sync_data_created_signal = sync_data_created_signal
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
    
    def add_sync_data_point(self, new_data_point):
        self.sync_data_queue.put(new_data_point)
        self.update_ui(new_data_point)
    
    def update_ui(self, dp):
        table_row_index = len(self.sync_data_queue.queue)-1
        
        # Ensure the row count is sufficient
        if table_row_index >= self.offline_data_table.rowCount():
            self.offline_data_table.setRowCount(table_row_index + 1)
        
        timestamp = dp.get('key-presses', {}).get('createdAt', '')

        for col, (key, val_obj) in enumerate(dp.items()):
            val = round(val_obj['amount'], 2) if key=='mouse-movements' else val_obj['count']
            cell = QTableWidgetItem(str(val))
            # Set cell values as read-only
            cell.setFlags(cell.flags() ^ Qt.ItemIsEditable)
        
            self.offline_data_table.setItem(table_row_index, col, cell)

        timestamp_formatted = datetime.fromisoformat(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        self.offline_data_table.setItem(table_row_index, 4, QTableWidgetItem(timestamp))

        self.offline_data_table.scrollToBottom()

    def sync_all_offline_data(self):
        pass
    
    def clear_all_offline_data(self):
        self.sync_data_queue = queue.Queue()
        self.offline_data_table.setRowCount(0)