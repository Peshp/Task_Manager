import pyqtgraph as pg
from collections import deque
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout
from widgets.tab_service import make_stat_column, build_pair_grid

class DiskTab(QWidget):
    MAX_POINTS = 60

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.disk_data = deque([0] * self.MAX_POINTS, maxlen=self.MAX_POINTS)

        self.disk_plot = pg.PlotWidget()
        self.disk_plot.setBackground("#1e1e1e")
        self.disk_plot.setYRange(0, 100)
        self.disk_plot.showGrid(x=True, y=True, alpha=0.2)
        self.disk_curve = self.disk_plot.plot(pen=pg.mkPen(color="#4A90D9", width=2))
        layout.addWidget(self.disk_plot)

        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(50)
        bottom_row.setContentsMargins(0, 20, 0, 0)

        dyn_col1 = make_stat_column(self, [("Active", "disk_active"), ("Read", "read_speed")])
        dyn_col2 = make_stat_column(self, [("Write", "write_speed"), ("Average responses", "avg_responses")])

        bottom_row.addLayout(dyn_col1)
        bottom_row.addLayout(dyn_col2)

        static_rows = [
            ("Capacity:", "total"),
            ("Used:", "used"),
            ("Free:", "free"),
        ]

        static_col = QVBoxLayout()
        static_col.setContentsMargins(0, 0, 0, 0)
        static_col.addLayout(build_pair_grid(self, static_rows))
        static_col.addStretch(1)

        bottom_row.addLayout(static_col)
        bottom_row.addStretch(1)   

        layout.addLayout(bottom_row)

    def update_data(self, data):
        disk_active = data['active']
        disk_read_speed = data['read']
        disk_write_speed = data['write']
        disk_avg_responses = data['avg_responses']

        self.disk_data.append(disk_active)

        self.disk_curve.setData(list(self.disk_data))
        self.disk_active_value.setText(f'{disk_active:.1f}%')
        self.read_speed_value.setText(f'{disk_read_speed:.2f} MB/s')
        self.write_speed_value.setText(f'{disk_write_speed:.2f}MB/s')
        self.avg_responses_value.setText(f'{disk_avg_responses:.1f}ms')
    
    def set_disk_capacity(self, data):
        self.total.setText(f'{data['total']:.2f} GB')
        self.used.setText(f'{data['used']:.2f} GB')
        self.free.setText(f'{data['free']:.2f} GB')