import pyqtgraph as pg
from collections import deque
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout

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

        bottom_container = QHBoxLayout()
        bottom_container.setSpacing(20)   

        left_main = QVBoxLayout()
        left_main.setSpacing(5)

        dynamic_grid = QHBoxLayout()
        dynamic_grid.setSpacing(10)

        dyn_col1 = QVBoxLayout()
        dyn_col1.setSpacing(4) 

        self.disk_label_title = QLabel("Active speed")
        self.disk_label_title.setStyleSheet("color: #9b9b9b; font-size: 14pt;")
        self.disk_label_speed = QLabel("Active speed")
        self.disk_label_speed.setStyleSheet("color: white; font-size: 22pt; font-weight: 300;")
        dyn_col1.addWidget(self.disk_label_title)
        dyn_col1.addWidget(self.disk_label_speed)
        dyn_col1.addSpacing(10)

        self.disk_title_read = QLabel('Read speed: 0 MB/s')
        self.disk_title_read.setStyleSheet("color: #9b9b9b; font-size: 14pt;")
        self.disk_label_read = QLabel("0%")
        self.disk_label_read.setStyleSheet("color: white; font-size: 22pt; font-weight: 300;")
        dyn_col1.addWidget(self.disk_title_read)
        dyn_col1.addWidget(self.disk_label_read)
        dyn_col1.addSpacing(10)

        dyn_col2 = QVBoxLayout()
        dyn_col2.setSpacing(4)   

        self.disk_title_write = QLabel('Read speed: 0 MB/s')
        self.disk_title_write.setStyleSheet("color: #9b9b9b; font-size: 14pt;")
        self.disk_label_write = QLabel("0%")
        self.disk_label_write.setStyleSheet("color: white; font-size: 22pt; font-weight: 300;")
        dyn_col2.addWidget(self.disk_title_write)
        dyn_col2.addWidget(self.disk_label_write)
        dyn_col2.addSpacing(10)

        self.disk_title_average = QLabel('Read speed: 0 MB/s')
        self.disk_title_average.setStyleSheet("color: #9b9b9b; font-size: 14pt;")
        self.disk_label_average = QLabel("0%")
        self.disk_label_average.setStyleSheet("color: white; font-size: 22pt; font-weight: 300;")
        dyn_col2.addWidget(self.disk_title_average)
        dyn_col2.addWidget(self.disk_label_average)
        dyn_col2.addSpacing(10)

        dynamic_grid.addLayout(dyn_col1)
        dynamic_grid.addLayout(dyn_col2)

        left_main.addLayout(dynamic_grid)

        right_main = QGridLayout()
        right_main.setHorizontalSpacing(50)
        right_main.setVerticalSpacing(0)

        static_rows = [
            ("Capacity:", "total"),
            ("Used:", "used"),
            ("Free:", "free"),
        ]

        left_column = QVBoxLayout()
        left_column.addLayout(self.build_pair_grid(static_rows))
        left_column.addSpacing(20)

        right_main.addLayout(left_column, 0, 0)

        right_main_wrapper = QVBoxLayout()
        right_main_wrapper.addLayout(right_main)
        right_main_wrapper.addStretch()

        bottom_container.addLayout(left_main, stretch=1)
        bottom_container.addLayout(right_main_wrapper, stretch=1)

        layout.addLayout(bottom_container)

    def update_data(self, data):
        disk_active = data['active']
        disk_read_speed = data['read']
        disk_write_speed = data['write']
        disk_avg_responses = data['avg_responses']

        self.disk_data.append(disk_active)

        self.disk_curve.setData(list(self.disk_data))
        self.disk_label_speed.setText(f'{disk_active:.1f}%')
        self.disk_label_read.setText(f'{disk_read_speed:.2f} MB/s')
        self.disk_label_write.setText(f'{disk_write_speed:.2f}MB/s')
        self.disk_label_average.setText(f'{disk_avg_responses:.1f}ms')
    
    def set_disk_capacity(self, data):
        self.total.setText(f'{data['total']:.2f} GB')
        self.used.setText(f'{data['used']:.2f} GB')
        self.free.setText(f'{data['free']:.2f} GB')

    def build_pair_grid(self, pairs):
        grid = QGridLayout()
        grid.setHorizontalSpacing(15)
        grid.setVerticalSpacing(6)
        for row, (label_text, attr_name) in enumerate(pairs):
            key_label = QLabel(label_text)
            key_label.setStyleSheet("color: #9b9b9b; font-size: 13pt;")

            value_label = QLabel("-")
            value_label.setStyleSheet("color: white; font-size: 13pt;")

            setattr(self, attr_name, value_label)

            grid.addWidget(key_label, row, 0)
            grid.addWidget(value_label, row, 1)
        grid.setColumnStretch(1, 1)
        return grid