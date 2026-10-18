import pyqtgraph as pg
from collections import deque
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout
from widgets.tab_service import build_pair_grid

class GPUTab(QWidget):
    MAX_POINTS = 60

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        self.gpu_data = deque([0] * self.MAX_POINTS, maxlen=self.MAX_POINTS)

        # ---- Header ----
        gpu_header = QHBoxLayout()
        self.gpu_label = QLabel("")
        self.gpu_label.setStyleSheet("color: white; font-size: 16pt; font-weight: 600;")

        self.gpu_vendor_label = QLabel("AMD")
        self.gpu_vendor_label.setStyleSheet("color: #dddddd; font-size: 14pt; font-weight: 600;")

        gpu_header.addWidget(self.gpu_label)
        gpu_header.addStretch()
        gpu_header.addWidget(self.gpu_vendor_label)
        layout.addLayout(gpu_header)

        # ---- Graph ----
        self.gpu_plot = pg.PlotWidget()
        self.gpu_plot.setBackground("#1e1e1e")
        self.gpu_plot.setYRange(0, 100)
        self.gpu_plot.showGrid(x=True, y=True, alpha=0.2)
        self.gpu_curve = self.gpu_plot.plot(
            list(self.gpu_data), pen=pg.mkPen(color="#9B59B6", width=2)
        )
        layout.addWidget(self.gpu_plot)

        bottom_container = QHBoxLayout()
        bottom_container.setSpacing(20)

        # ---------- LEFT MAIN COLUMN (dynamic) ----------
        left_main = QVBoxLayout()
        left_main.setSpacing(5)

        dynamic_grid = QHBoxLayout()
        dynamic_grid.setSpacing(10)

        dyn_col1 = QVBoxLayout()
        dyn_col1.setSpacing(4)

        real_time_2 = [
             ("Voltage (mV)", 'voltage'),
             ("Core Clock (MHz)", 'core_clock'),
             ("Memory Clock (MHz)", 'memory_clock'),
             ('Fan Speed (RPM)', 'fan_speed')
        ]

        self.temp_edge_title = QLabel("Temperature Edge (°C)")
        self.temp_edge_title.setStyleSheet("color: #9b9b9b; font-size: 14pt;")
        self.temp_edge = QLabel("0")
        self.temp_edge.setStyleSheet("color: white; font-size: 16pt;")
        dyn_col1.addWidget(self.temp_edge_title)
        dyn_col1.addWidget(self.temp_edge)
        dyn_col1.addSpacing(10)

        self.power_limit_title = QLabel("Up time")
        self.power_limit_title.setStyleSheet("color: #9b9b9b; font-size: 14pt;")
        self.power_limit = QLabel("00:00:00")
        self.power_limit.setStyleSheet("color: white; font-size: 16pt;")
        dyn_col1.addWidget(self.power_limit_title)
        dyn_col1.addWidget(self.power_limit)
        dyn_col1.addStretch()

        self.voltage_title = QLabel("Voltage (mV)")
        self.voltage_title.setStyleSheet("color: #9b9b9b; font-size: 14pt;")
        self.voltage = QLabel("00:00:00")
        self.voltage.setStyleSheet("color: white; font-size: 16pt;")
        dyn_col1.addWidget(self.voltage_title)
        dyn_col1.addWidget(self.voltage)
        dyn_col1.addStretch()

        dyn_col2 = QVBoxLayout()
        dyn_col2.setSpacing(4) 

        self.core_clock_title = QLabel("Core Clock (MHz)")
        self.core_clock_title.setStyleSheet("color: #9b9b9b; font-size: 14pt;")
        self.core_clock = QLabel("0.00 GHz")
        self.core_clock.setStyleSheet("color: white; font-size: 22pt; font-weight: 300;")
        dyn_col2.addWidget(self.core_clock_title)
        dyn_col2.addWidget(self.core_clock)
        dyn_col2.addSpacing(10)

        self.memory_clock_title = QLabel("Memory Clock (MHz)")
        self.memory_clock_title.setStyleSheet("color: #9b9b9b; font-size: 14pt;")
        self.memory_clock = QLabel("0.00 GHz")
        self.memory_clock.setStyleSheet("color: white; font-size: 22pt; font-weight: 300;")
        dyn_col2.addWidget(self.memory_clock_title)
        dyn_col2.addWidget(self.memory_clock)
        dyn_col2.addSpacing(10)

        self.fan_speed_title = QLabel("Fan Speed (RPM)")
        self.fan_speed_title.setStyleSheet("color: #9b9b9b; font-size: 14pt;")
        self.fan_speed = QLabel("0.00 GHz")
        self.fan_speed.setStyleSheet("color: white; font-size: 22pt; font-weight: 300;")
        dyn_col2.addWidget(self.fan_speed_title)
        dyn_col2.addWidget(self.fan_speed)
        dyn_col2.addSpacing(10)

        dynamic_grid.addLayout(dyn_col1)
        dynamic_grid.addLayout(dyn_col2)

        left_main.addLayout(dynamic_grid)
        left_main.addStretch()

        # ---------- RIGHT MAIN COLUMN (dynamic) ----------
        right_main = QGridLayout()
        right_main.setHorizontalSpacing(50)
        right_main.setVerticalSpacing(0)

        static_rows = [
            ("VRAM Total (MiB)", "vram_total_mib"),
            ("GTT", "gtt"),
            ("Performarce Level", "perf"),
            ("Max Power Limit", "cap_max"),
            ("Default Power Limit", "cap_def"),
            ("Temperature Critical (°C)", "temp_critical_c"),
            ("Temperature Emergency (°C)", "temp_emergency_c"),
            ("Fan RPM Min", "fan_rpm_min"),
            ("Fan RPM Max", "fan_rpm_max"),
        ]

        left_column = QVBoxLayout()
        left_column.addSpacing(20)
        left_column.addStretch()

        right_column = self.build_pair_grid(static_rows)

        right_main.addLayout(left_column, 0, 0)
        right_main.addLayout(right_column, 0, 1)
        right_main.setColumnStretch(1, 1)

        right_main_wrapper = QVBoxLayout()
        right_main_wrapper.addLayout(right_main)
        right_main_wrapper.addStretch()

        bottom_container.addLayout(left_main, stretch=1)
        bottom_container.addLayout(right_main_wrapper, stretch=1)

        layout.addLayout(bottom_container)

    def update_data(self, data):
        gpu_percent = data['GPU Load (%)']
        self.gpu_label.setText(f'{gpu_percent:.0f}%')

        self.temp_edge.setText(f"{data.get('Temperature Edge (°C)') or 0:.1f} °C")
        self.power_limit.setText(f"{data.get('Power Limit (W)') or 0:.0f} W")

        self.voltage.setText(f"{data.get('Voltage (mV)') or 0:.0f} mV")
        self.core_clock.setText(f"{data.get('Core Clock (MHz)') or 0:.0f} MHz")
        self.memory_clock.setText(f"{data.get('Memory Clock (MHz)') or 0:.0f} MHz")
        self.fan_speed.setText(f"{data.get('Fan Speed (RPM)') or 0:.0f} RPM")

        self.gpu_data.append(gpu_percent)
        self.gpu_curve.setData(list(self.gpu_data))
        self.gpu_label.setText(f'GPU: {gpu_percent}')
    
    def get_static(self, data):
        self.gpu_vendor_label.setText(str(data.get('GPU')))

        self.vram_total_mib.setText(str(data.get("VRAM")))
        self.gtt.setText(str(data.get("GTT")))
        self.perf.setText(str(data.get("Perf level")))

        self.cap_max.setText(str(data.get("Power cap max")))
        self.cap_def.setText(str(data.get("Power cap def")))

        self.temp_critical_c.setText(f"{data.get('Temperature Critical (°C)') or 0:.0f} °C")
        self.temp_emergency_c.setText(f"{data.get('Temperature Emergency (°C)') or 0:.0f} °C")

        self.fan_rpm_min.setText(f"{data.get('Fan RPM Min') or 0:.0f} RPM")
        self.fan_rpm_max.setText(f"{data.get('Fan RPM Max') or 0:.0f} RPM")

    def build_pair_dym(self, pairs):
        dyn_col1 = QGridLayout()
        dyn_col1.setHorizontalSpacing(15)
        dyn_col1.setVerticalSpacing(6)

        for row, (label_text, attr_name) in enumerate(pairs):
            key_label = QLabel(label_text)
            key_label.setStyleSheet("color: #9b9b9b; font-size: 14pt;")

            value_label = QLabel("")
            value_label.setStyleSheet("color: white; font-size: 16pt; font-weight: 300;")

            setattr(self, attr_name, value_label)
            dyn_col1.addWidget(key_label, row, 0)
            dyn_col1.addWidget(value_label, row, 1)

        dyn_col1.setColumnStretch(1, 1)
        return dyn_col1


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
        




