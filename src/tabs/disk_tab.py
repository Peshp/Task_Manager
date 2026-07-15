import pyqtgraph as pg
from collections import deque
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout

class DiskTab(QWidget):
    MAX_POINTS = 60

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.disk_data = deque([0] * self.MAX_POINTS, maxlen=self.MAX_POINTS)

        disk_header = QHBoxLayout()
        self.disk_label = QLabel("Active: 0%")
        self.disk_label.setStyleSheet("color: white; font-size: 14pt; font-weight: 600;")

        disk_header.addWidget(self.disk_label)
        disk_header.addStretch()
        layout.addLayout(disk_header)

        self.disk_plot = pg.PlotWidget()
        self.disk_plot.setBackground("#1e1e1e")
        self.disk_plot.setYRange(0, 100)
        self.disk_plot.showGrid(x=True, y=True, alpha=0.2)
        self.disk_curve = self.disk_plot.plot(pen=pg.mkPen(color="#4A90D9", width=2))
        layout.addWidget(self.disk_plot)

        self.stats_container = QHBoxLayout()
        self.stats_container.setContentsMargins(20, 8, 20, 8)  
        self.stats_container.setSpacing(30)    

        left_column = QVBoxLayout()
        left_column.setContentsMargins(0, 0, 0, 0)
        left_column.setSpacing(4)   

        self.disk_label_read = QLabel('Read speed: 0 MB/s')
        self.disk_label_read.setStyleSheet("color: white; font-size: 14pt; font-weight: 600;")
        left_column.addWidget(self.disk_label_read)

        self.disk_label_write = QLabel('Write speed: 0 MB/s')
        self.disk_label_write.setStyleSheet("color: white; font-size: 14pt; font-weight: 600;")
        left_column.addWidget(self.disk_label_write)

        self.disk_label_average = QLabel('Average response: 0 ms')
        self.disk_label_average.setStyleSheet("color: white; font-size: 14pt; font-weight: 600;")
        left_column.addWidget(self.disk_label_average)

        right_column = QVBoxLayout()
        right_column.setContentsMargins(0, 0, 0, 0)
        right_column.setSpacing(4)

        self.disk_label_capacity = QLabel('Total: 0 MB')
        self.disk_label_capacity.setStyleSheet("color: white; font-size: 14pt; font-weight: 600;")
        right_column.addWidget(self.disk_label_capacity)

        self.disk_label_used = QLabel('Used: 0 MB')
        self.disk_label_used.setStyleSheet("color: white; font-size: 14pt; font-weight: 600;")
        right_column.addWidget(self.disk_label_used)

        self.disk_label_free = QLabel('Free: 0 MB')
        self.disk_label_free.setStyleSheet("color: white; font-size: 14pt; font-weight: 600;")
        right_column.addWidget(self.disk_label_free)

        self.stats_container.addLayout(left_column)
        self.stats_container.addStretch()
        self.stats_container.addLayout(right_column)

        layout.addLayout(self.stats_container)

    def update_data(self, data):
        disk_active = data['active']
        disk_read_speed = data['read']
        disk_write_speed = data['write']
        disk_avg_responses = data['avg_responses']

        self.disk_data.append(disk_active)

        self.disk_curve.setData(list(self.disk_data))
        self.disk_label.setText(f'Active: {disk_active:.1f}%')
        self.disk_label_read.setText(f'Read speed: {disk_read_speed:.2f} MB/s')
        self.disk_label_write.setText(f'Write speed: {disk_write_speed:.2f}MB/s')
        self.disk_label_average.setText(f'Average speed: {disk_avg_responses:.1f}ms')
    
    def set_disk_capacity(self, data):
        self.disk_label_capacity.setText(f'Total: {data['total']:.2f} GB')
        self.disk_label_used.setText(f'Used: {data['used']:.2f} GB')
        self.disk_label_free.setText(f'Free: {data['free']:.2f} GB')