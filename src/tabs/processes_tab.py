from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QSizePolicy, QAbstractItemView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


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

        self.table.setStyleSheet(f"""
            QTableWidget {{
                background: #1a1a1a;
                alternate-background-color: #202020;
                color: #f0f0f0;
                gridline-color: transparent;
                border: 1px solid #333333;
                border-radius: 8px;
                font-size: {self.CELL_FONT_SIZE}px;
            }}
            QTableWidget::item {{
                padding-left: 12px;
                border: none;
            }}
            QHeaderView::section {{
                background: #242424;
                color: #9e9e9e;
                padding-left: 12px;
                border: none;
                border-bottom: 1px solid #333333;
                font-size: {self.HEADER_FONT_SIZE}px;
                font-weight: 600;
            }}
            QTableWidget::item:selected {{
                background: #2C4A6E;
                color: #ffffff;
            }}
            QTableWidget::item:hover {{
                background: #262626;
            }}

            /* ---- Vertical scrollbar ---- */
            QScrollBar:vertical {{
                background: #1a1a1a;
                width: 10px;
                margin: 0px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background: #4A90D9;
                min-height: 24px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: #63A6E8;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}

            /* ---- Horizontal scrollbar ---- */
            QScrollBar:horizontal {{
                background: #1a1a1a;
                height: 10px;
                margin: 0px;
                border-radius: 5px;
            }}
            QScrollBar::handle:horizontal {{
                background: #4A90D9;
                min-width: 24px;
                border-radius: 5px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background: #63A6E8;
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
                background: none;
            }}
        """)

        layout.addWidget(self.table)

    def update_data(self, cpu_rows):
        if not cpu_rows:
            self.table.setRowCount(0)
            return

        columns = list(cpu_rows[0].keys())
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

