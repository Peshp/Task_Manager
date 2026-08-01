import pyqtgraph as pg
from collections import deque
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout
from widgets.tab_service import make_stat_column, build_pair_grid

class MemoryTab(QWidget):
    MAX_POINTS = 60

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        self.mem_data = deque([0] * self.MAX_POINTS, maxlen=self.MAX_POINTS)

        mem_header = QHBoxLayout()
        self.mem_label = QLabel("")
        self.mem_label.setStyleSheet("color: white; font-size: 14pt; font-weight: 600;")

        self.disk_label_size = QLabel("")
        self.disk_label_size.setStyleSheet("color: #dddddd; font-size: 12pt;")

        mem_header.addWidget(self.mem_label)
        mem_header.addStretch()
        mem_header.addWidget(self.disk_label_size)
        layout.addLayout(mem_header)

        self.mem_plot = pg.PlotWidget()
        self.mem_plot.setBackground("#1e1e1e")
        self.mem_plot.setYRange(0, 100)
        self.mem_plot.showGrid(x=True, y=True, alpha=0.2)
        self.mem_curve = self.mem_plot.plot(
            list(self.mem_data), pen=pg.mkPen(color="#9B59B6", width=2)
        )
        layout.addWidget(self.mem_plot)

        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(50)
        bottom_row.setContentsMargins(0, 20, 0, 0)

        dyn_col1 = make_stat_column(self, [("Active", "active_memory"), ("Cached", "cached_memory")])
        dyn_col2 = make_stat_column(self, [("Free", "free_memory"), ("Shared", "shared_memory")])

        bottom_row.addLayout(dyn_col1)
        bottom_row.addLayout(dyn_col2)

        static_rows = [
            ("Speed:", "active_speed"),
            ("Form factor:", "form_factor"),
            ("Location:", "location"),
            ("Capacity:", "capacity"),
        ]
        static_col = QVBoxLayout()
        static_col.setContentsMargins(0, 0, 0, 0)
        static_col.addLayout(build_pair_grid(self, static_rows))
        static_col.addStretch(1)

        bottom_row.addLayout(static_col)
        bottom_row.addStretch(1)   

        layout.addLayout(bottom_row)
    
    def update_data(self, data):
        mem_percent = data['memory'].percent
        active = data['active']
        free = data['free']
        cached = data['cached']
        shared = data['shared']

        self.active_memory_value.setText(f'{active:.2f} GB')
        self.cached_memory_value.setText(f'{free:.2f} GB')
        self.free_memory_value.setText(f'{cached:.2f} GB')
        self.shared_memory_value.setText(f'{shared:.2f} GB')

        self.mem_data.append(mem_percent)

        self.mem_curve.setData(list(self.mem_data)) 
        self.mem_label.setText(f'Memory: {mem_percent:.1f}%')
    
    def get_memory_stats(self, data):
        self.active_speed.setText(f"{data['Configured Memory Speed']}")
        self.form_factor.setText(f"{data['Form Factor']}")
        self.location.setText(f"{data['Locator']}")
        self.capacity.setText(f"{data['Maximum Capacity']}")




