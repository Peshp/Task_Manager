import pyqtgraph as pg
from collections import deque
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout

class CPUTab(QWidget):
    MAX_POINTS = 60

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        self.cpu_data = deque([0] * self.MAX_POINTS, maxlen=self.MAX_POINTS)

        # ---- Header ----
        cpu_header = QHBoxLayout()
        self.cpu_label = QLabel("CPU")
        self.cpu_label.setStyleSheet("color: white; font-size: 16pt; font-weight: 600;")

        self.cpu_vendor_label = QLabel("Vendor")
        self.cpu_vendor_label.setStyleSheet("color: #dddddd; font-size: 14pt; font-weight: 600;")

        cpu_header.addWidget(self.cpu_label)
        cpu_header.addStretch()
        cpu_header.addWidget(self.cpu_vendor_label)
        layout.addLayout(cpu_header)

        # ---- Graph ----
        self.cpu_plot = pg.PlotWidget()
        self.cpu_plot.setBackground("#1e1e1e")
        self.cpu_plot.setYRange(0, 100)
        self.cpu_plot.showGrid(x=True, y=True, alpha=0.2)
        self.cpu_curve = self.cpu_plot.plot(
            list(self.cpu_data), pen=pg.mkPen(color="#9B59B6", width=2)
        )
        layout.addWidget(self.cpu_plot)

        bottom_container = QHBoxLayout()
        bottom_container.setSpacing(40)

        # ---------- LEFT MAIN COLUMN (dynamic) ----------
        left_main = QVBoxLayout()
        left_main.setSpacing(15)

        dynamic_grid = QHBoxLayout()
        dynamic_grid.setSpacing(30)

        dyn_col1 = QVBoxLayout()
        dyn_col1.setSpacing(4)

        self.utilization_title = QLabel("Utilization")
        self.utilization_title.setStyleSheet("color: #9b9b9b; font-size: 14pt;")
        self.utilization = QLabel("0%")
        self.utilization.setStyleSheet("color: white; font-size: 22pt; font-weight: 300;")
        dyn_col1.addWidget(self.utilization_title)
        dyn_col1.addWidget(self.utilization)
        dyn_col1.addSpacing(10)

        self.processes_title = QLabel("Processes")
        self.processes_title.setStyleSheet("color: #9b9b9b; font-size: 14pt;")
        self.processes = QLabel("0")
        self.processes.setStyleSheet("color: white; font-size: 16pt;")
        dyn_col1.addWidget(self.processes_title)
        dyn_col1.addWidget(self.processes)
        dyn_col1.addSpacing(10)

        self.uptime_title = QLabel("Up time")
        self.uptime_title.setStyleSheet("color: #9b9b9b; font-size: 14pt;")
        self.uptime = QLabel("00:00:00")
        self.uptime.setStyleSheet("color: white; font-size: 16pt;")
        dyn_col1.addWidget(self.uptime_title)
        dyn_col1.addWidget(self.uptime)
        dyn_col1.addStretch()

        dyn_col2 = QVBoxLayout()
        dyn_col2.setSpacing(4)   

        self.speed_title = QLabel("Speed")
        self.speed_title.setStyleSheet("color: #9b9b9b; font-size: 14pt;")
        self.current_speed = QLabel("0.00 GHz")
        self.current_speed.setStyleSheet("color: white; font-size: 22pt; font-weight: 300;")
        dyn_col2.addWidget(self.speed_title)
        dyn_col2.addWidget(self.current_speed)
        dyn_col2.addSpacing(10)

        self.threads_title = QLabel("Threads")
        self.threads_title.setStyleSheet("color: #9b9b9b; font-size: 14pt;")
        self.threads = QLabel("0")
        self.threads.setStyleSheet("color: white; font-size: 22pt;")
        dyn_col2.addWidget(self.threads_title)
        dyn_col2.addWidget(self.threads)
        dyn_col2.addSpacing(10)

        self.handles_title = QLabel("Handles")
        self.handles_title.setStyleSheet("color: #9b9b9b; font-size: 14pt;")
        self.handles = QLabel("0")
        self.handles.setStyleSheet("color: white; font-size: 16pt;")
        dyn_col2.addWidget(self.handles_title)
        dyn_col2.addWidget(self.handles)
        dyn_col2.addStretch()

        dynamic_grid.addLayout(dyn_col1)
        dynamic_grid.addLayout(dyn_col2)

        left_main.addLayout(dynamic_grid)
        left_main.addStretch()

        right_main = QGridLayout()
        right_main.setHorizontalSpacing(15)
        right_main.setVerticalSpacing(6)

        static_rows = [
            ("Base speed:", "base_speed"),
            ("Sockets:", "sockets"),
            ("Cores:", "physical"),
            ("Logical processors:", "logical"),
            ("Virtualization:", "virtualization"),
            ("L1 cache:", "l1_cache"),
            ("L2 cache:", "l2_cache"),
            ("L3 cache:", "l3_cache"),
        ]

        for row, (label_text, attr_name) in enumerate(static_rows):
            key_label = QLabel(label_text)
            key_label.setStyleSheet("color: #9b9b9b; font-size: 13pt;")

            value_label = QLabel("-")
            value_label.setStyleSheet("color: white; font-size: 13pt;")

            setattr(self, attr_name, value_label)

            right_main.addWidget(key_label, row, 0)
            right_main.addWidget(value_label, row, 1)

        right_main.setColumnStretch(1, 1)

        right_main_wrapper = QVBoxLayout()
        right_main_wrapper.addLayout(right_main)
        right_main_wrapper.addStretch()

        bottom_container.addLayout(left_main, stretch=1)
        bottom_container.addLayout(right_main_wrapper, stretch=1)

        layout.addLayout(bottom_container)

    def update_data(self, data):
        cpu_percent = data['utilization']
        current_speed = data['current_speed']

        processes = data.get('processes', 0)
        threads = data.get('threads', 0)
        handles = data.get('handles', 0)

        self.utilization.setText(f'{cpu_percent:.0f}%')
        self.current_speed.setText(f'{current_speed:.2f} GHz')
        self.processes.setText(str(processes))
        self.threads.setText(str(threads))
        self.handles.setText(str(handles))

        self.cpu_data.append(cpu_percent)
        self.cpu_curve.setData(list(self.cpu_data))
    
    def get_static(self, data):
        base_speed = data['base_speed']
        physical = data['psyhical']
        logical = data['logical']
        sockets = data.get('sockets', 1)
        virtualization = data.get('virtualization', 'N/A')
        l1_cache = data.get('l1_cache', 'N/A')
        l2_cache = data.get('l2_cache', 'N/A')
        l3_cache = data.get('l3_cache', 'N/A')

        self.cpu_vendor_label.setText(data['Model name'])
        self.uptime.setText(data['uptime'])
        self.base_speed.setText(f'{base_speed:.2f} GHz')
        self.sockets.setText(str(sockets))
        self.physical.setText(str(physical))
        self.logical.setText(str(logical))
        self.virtualization.setText(str(virtualization))
        self.l1_cache.setText(str(l1_cache))
        self.l2_cache.setText(str(l2_cache))
        self.l3_cache.setText(str(l3_cache))




