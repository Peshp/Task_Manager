import pyqtgraph as pg
from collections import deque
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget

class MemoryTab(QWidget):
    MAX_POINTS = 60

    def __init__(self, parent = None):
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

        self.stats_container = QHBoxLayout()
        self.stats_container.setContentsMargins(20, 8, 20, 8)  
        self.stats_container.setSpacing(30)    

        left_column = QVBoxLayout()
        left_column.setContentsMargins(0, 0, 0, 0)
        left_column.setSpacing(6)

        self.active_memory = QLabel('')
        self.active_memory.setStyleSheet("color: white; font-size: 14pt; font-weight: 600;")
        left_column.addWidget(self.active_memory)

        self.free_memory = QLabel('')
        self.free_memory.setStyleSheet("color: white; font-size: 14pt; font-weight: 600;")
        left_column.addWidget(self.free_memory)

        self.cached_memory = QLabel('')
        self.cached_memory.setStyleSheet("color: white; font-size: 14pt; font-weight: 600;")
        left_column.addWidget(self.cached_memory)

        self.shared_memory = QLabel('')
        self.shared_memory.setStyleSheet("color: white; font-size: 14pt; font-weight: 600;")
        left_column.addWidget(self.shared_memory)

        self.stats_container.addLayout(left_column)

        right_column = QVBoxLayout()
        right_column.setContentsMargins(0, 0, 0, 0)
        right_column.setSpacing(4)

        self.disk_label_speed = QLabel('')
        self.disk_label_speed.setStyleSheet("color: white; font-size: 14pt; font-weight: 600;")
        right_column.addWidget(self.disk_label_speed)

        self.disk_label_form = QLabel('')
        self.disk_label_form.setStyleSheet("color: white; font-size: 14pt; font-weight: 600;")
        right_column.addWidget(self.disk_label_form)

        self.disk_label_slots = QLabel('')
        self.disk_label_slots.setStyleSheet("color: white; font-size: 14pt; font-weight: 600;")
        right_column.addWidget(self.disk_label_slots)

        self.stats_container.addLayout(right_column)
        layout.addLayout(self.stats_container)
    
    def update_data(self, data):
        mem_percent = data['memory'].percent
        active = data['active']
        free = data['free']
        cached = data['cached']
        shared = data['shared']

        self.active_memory.setText(f'Active {active:.2F} GB')
        self.free_memory.setText(f'Free {free:.2f} GB')
        self.cached_memory.setText(f'Cached: {cached:.2f} GB')
        self.shared_memory.setText(f'Shared: {shared:.2f} GB')

        self.mem_data.append(mem_percent)

        self.mem_curve.setData(list(self.mem_data)) 
        self.mem_label.setText(f'Memory: {mem_percent:.1f}%')
    
    def get_memory_stats(self, data):
        self.disk_label_speed.setText(f"Speed: {data['Configured Memory Speed']}")
        self.disk_label_form.setText(f"Form factor: {data['Form Factor']}")
        self.disk_label_slots.setText(f"Location: slot {data['Locator']}")
        self.disk_label_size.setText(f"Capacity: {data['Maximum Capacity']}")




