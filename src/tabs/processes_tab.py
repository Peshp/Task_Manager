import os
import subprocess
import signal

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QSizePolicy, QAbstractItemView, QMenu
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QAction


class ProcessesTab(QWidget):
    MAX_POINTS = 60

    HEADER_FONT_SIZE = 15
    CELL_FONT_SIZE = 15
    FONT_FAMILY = "Segoe UI"
    ROW_HEIGHT = 44

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.pid_to_path = {}
        self.pid_col_idx = 0    

        self.table = QTableWidget()
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.verticalHeader().setVisible(False)
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setDefaultSectionSize(self.ROW_HEIGHT)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        header.setFixedHeight(40)

        header_font = QFont(self.FONT_FAMILY, self.HEADER_FONT_SIZE)
        header_font.setBold(True)
        header.setFont(header_font)

        cell_font = QFont(self.FONT_FAMILY, self.CELL_FONT_SIZE)
        self.table.setFont(cell_font)

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #2b2b2b;
                color: #ffffff;
                gridline-color: #3a3a3a;
                border: none;
                alternate-background-color: #323232;
                selection-background-color: #334e68; /* Dark Blue Grey */
                selection-color: #ffffff;
            }
            QTableWidget::item:hover {
                background-color: #486581; /* Lighter hover color */
            }
            QTableWidget::item:selected {
                background-color: #334e68; /* Dark Blue Grey */
                color: #ffffff;
            }
            QHeaderView::section {
                background-color: #1f1f1f;
                color: #ffffff;
                padding-left: 8px;
                border: none;
                border-bottom: 2px solid #334e68; /* Dark Blue Grey border */
            }
            QScrollBar:vertical {
                background: #2b2b2b;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #334e68; /* Dark Blue Grey handle */
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: #486581; /* Lighter handle on hover */
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        layout.addWidget(self.table)

    def update_data(self, cpu_rows):
        columns = [k for k in list(cpu_rows[0].keys()) if k != 'Path']
        self.pid_to_path = {row["PID"]: row.get("Path", "") for row in cpu_rows}
        
        if "PID" in columns:
            self.pid_col_idx = columns.index("PID")

        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        self.table.setRowCount(len(cpu_rows))

        for row_idx, row_data in enumerate(cpu_rows):
            for col_idx, key in enumerate(columns):
                value = row_data[key]
                if key == 'CPU%':
                    text = f'{value:.2f}%'
                elif key == 'Mem(MB)':
                    text = f'{value:.2f}'
                else:
                    text = str(value)

                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setData(Qt.ItemDataRole.UserRole, value)
                self.table.setItem(row_idx, col_idx, item)

    def contextMenuEvent(self, event):
        pos_in_table = self.table.viewport().mapFromGlobal(event.globalPos())
        item = self.table.itemAt(pos_in_table)

        row = item.row()
        self.table.selectRow(row)

        menu = QMenu(self)
        open_location_action = menu.addAction('Open file location')
        open_location_action.triggered.connect(lambda: self.open_file_location(row))

        end_task_action = menu.addAction('En task')
        end_task_action.triggered.connect(lambda: self.end_task(row))
        
        menu.exec(event.globalPos())

    def open_file_location(self, row):
        pid_item = self.table.item(row, self.pid_col_idx)
        try:
            pid = int(pid_item.text())
        except ValueError:
            return

        path = self.pid_to_path.get(pid, "")
        folder = os.path.dirname(path)
        subprocess.Popen(["xdg-open", folder])

    def end_task(self, row):
        pid_item = self.table.item(row, self.pid_col_idx) 
        try:
            pid = int(pid_item.text())
        except ValueError:
            return

        try:
            os.kill(pid, signal.SIGTERM)
        except PermissionError:
            os.kill(pid, signal.SIGKILL)

        self.pid_to_path.pop(pid, None)
        self.table.removeRow(row)