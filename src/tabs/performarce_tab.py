import pyqtgraph as pg
from collections import deque
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout

class PerformarceTab(QWidget):
    MAX_POINTS = 60

    def __init__(self, parent = None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.cpu_data = deque([0] * self.MAX_POINTS, maxlen=self.MAX_POINTS)
        self.mem_data = deque([0] * self.MAX_POINTS, maxlen=self.MAX_POINTS)

        # CPU:
        cpu_header = QHBoxLayout()
        self.cpu_label = QLabel("CPU: 0%")
        self.cpu_label.setStyleSheet("color: white; font-size: 14pt; font-weight: 600;")

        self.cpu_name_label = QLabel("")
        self.cpu_name_label.setStyleSheet("color: #dddddd; font-size: 12pt;")

        cpu_header.addWidget(self.cpu_label)
        cpu_header.addStretch()
        cpu_header.addWidget(self.cpu_name_label)
        layout.addLayout(cpu_header)

        self.cpu_plot = pg.PlotWidget()
        self.cpu_plot.setBackground("#1e1e1e")
        self.cpu_plot.setYRange(0, 100)
        self.cpu_plot.showGrid(x=True, y=True, alpha=0.2)
        self.cpu_curve = self.cpu_plot.plot(pen=pg.mkPen(color="#4A90D9", width=2))
        layout.addWidget(self.cpu_plot)

        # Memory:
        mem_header = QHBoxLayout()
        self.mem_label = QLabel("Memory: 0%")
        self.mem_label.setStyleSheet("color: white; font-size: 14pt; font-weight: 600;")

        self.memory_capacity = QLabel("")
        self.memory_capacity.setStyleSheet("color: #dddddd; font-size: 12pt;")

        mem_header.addWidget(self.mem_label)
        mem_header.addStretch()
        mem_header.addWidget(self.memory_capacity)

        layout.addLayout(mem_header)

        self.mem_plot = pg.PlotWidget()
        self.mem_plot.setBackground("#1e1e1e")
        self.mem_plot.setYRange(0, 100)
        self.mem_plot.showGrid(x=True, y=True, alpha=0.2)
        self.mem_curve = self.mem_plot.plot(
            list(self.mem_data), pen=pg.mkPen(color="#9B59B6", width=2)
        )
        layout.addWidget(self.mem_plot)


    def update_data(self, data):
        cpu_percent = data['cpu']
        mem_percent = data['memory'].percent

        self.cpu_data.append(cpu_percent)
        self.mem_data.append(mem_percent)

        self.cpu_curve.setData(list(self.cpu_data))
        self.mem_curve.setData(list(self.mem_data)) 
        self.cpu_label.setText(f'CPU: {cpu_percent:.1f}%')
        self.mem_label.setText(f'Memory: {mem_percent:.1f}%')
    
    def set_cpu_name(self, cpu_name):
        self.cpu_name_label.setText(cpu_name)
    
    def set_mem_capacity(self, gb):
        self.memory_capacity.setText(str(gb))