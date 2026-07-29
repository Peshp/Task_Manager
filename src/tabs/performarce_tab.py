import pyqtgraph as pg
from collections import deque
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout

class PerformarceTab(QWidget):
    MAX_POINTS = 60

    def __init__(self, parent = None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        self.cpu_data = deque([0] * self.MAX_POINTS, maxlen=self.MAX_POINTS)
        self.mem_data = deque([0] * self.MAX_POINTS, maxlen=self.MAX_POINTS)
        self.net_data = deque([0] * self.MAX_POINTS, maxlen=self.MAX_POINTS)
        self.disk_data = deque([0] * self.MAX_POINTS, maxlen=self.MAX_POINTS)

        # CPU:
        cpu_plot = self.create_plot('cpu')
        self.layout.addWidget(cpu_plot)

        # Memory:
        mem_plot = self.create_plot('mem')
        self.layout.addWidget(mem_plot)

        # Network:
        net_plot = self.create_plot('net')
        self.layout.addWidget(net_plot)

        # Disk:
        self.create_plot('disk')


    def update_data(self, data):
        cpu_percent = data['cpu']
        mem_percent = data['memory'].percent

        self.cpu_data.append(cpu_percent)
        self.mem_data.append(mem_percent)

        self.cpu_curve.setData(list(self.cpu_data))
        self.mem_curve.setData(list(self.mem_data)) 
        self.cpu_label.setText(f'CPU: {cpu_percent:.1f}%')
        self.mem_label.setText(f'Memory: {mem_percent:.1f}%')

    def net_update_data(self, data):
        download_mbps = data['download_mbps']
        self.net_data.append(download_mbps)
        self.net_curve.setData(list(self.net_data))
        self.net_label.setText(f'Network: {download_mbps:.1f}%')

    def disk_update_data(self, data):
        disk_active = data['active']
        self.disk_data.append(disk_active)
        self.disk_curve.setData(list(self.disk_data))
        self.disk_label.setText(f'Disk: {disk_active:.1f}%')
    
    def set_cpu_name(self, cpu_name):
        self.cpu_name_label.setText(cpu_name)

    def create_plot(self, name: str):
        header = QHBoxLayout()

        value_label = QLabel()
        value_label.setStyleSheet("color: white; font-size: 14pt; font-weight: 600;")

        name_label = QLabel("")
        name_label.setStyleSheet("color: #dddddd; font-size: 12pt;")

        header.addWidget(value_label)
        header.addStretch()
        header.addWidget(name_label)
        self.layout.addLayout(header)

        plot = pg.PlotWidget()
        plot.setBackground("#1e1e1e")
        plot.setYRange(0, 100)
        plot.showGrid(x=True, y=True, alpha=0.2)
        curve = plot.plot(pen=pg.mkPen(color='#9B59B6', width=2))

        self.layout.addWidget(plot)

        setattr(self, f"{name}_label", value_label)
        setattr(self, f"{name}_name_label", name_label)
        setattr(self, f"{name}_plot", plot)
        setattr(self, f"{name}_curve", curve)