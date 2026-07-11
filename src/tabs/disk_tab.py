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

        self.stats_widget = QHBoxLayout()
        self.disk_label_read = QLabel('Read speed: 0MB/s')
        self.disk_label_read.setStyleSheet("color: white; font-size: 14pt; font-weight: 600;")
        self.stats_widget.addWidget(self.disk_label_read)
        self.stats_widget.addStretch()

        self.disk_label_write = QLabel('Write speed: 0MB/s')
        self.disk_label_write.setStyleSheet("color: white; font-size: 14pt; font-weight: 600;")
        self.stats_widget.addWidget(self.disk_label_write)
        self.stats_widget.addStretch()

        self.disk_label_average = QLabel('Average speed: 0ms')
        self.disk_label_average.setStyleSheet("color: white; font-size: 14pt; font-weight: 600;")
        self.stats_widget.addWidget(self.disk_label_average)
        self.stats_widget.addStretch()
        layout.addLayout(self.stats_widget)

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