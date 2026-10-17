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

        real_time_1 = [
            ('Fan Duty (%)', 'fan_duty'),
            ('Performance Mode', 'performarce'),
            ('Temperature Edge (°C)', 'temp_edge'),
            ('Power Draw (W)', 'power_draw'),
            ('Power Limit (W)', 'power_limit')
        ]

        real_time_2 = [
             ("Voltage (mV)", 'voltage'),
             ("Core Clock (MHz)", 'core_clock'),
             ("Memory Clock (MHz)", 'memory_clock'),
             ('Fan Speed (RPM)', 'fan_speed')
        ]

        dynamic_grid.addLayout(self.build_pair_dym(real_time_1))
        dynamic_grid.addLayout(self.build_pair_dym(real_time_2))

        left_main.addLayout(dynamic_grid)
        left_main.addStretch()

        # ---------- RIGHT MAIN COLUMN (dynamic) ----------
        right_main = QGridLayout()
        right_main.setHorizontalSpacing(50)
        right_main.setVerticalSpacing(0)

        static_rows = [
            ("VBIOS Version", "vbios_version"),
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

        vendor_rows = [
            ("GPU Model", "gpu_model"),
            ("GPU Vendor", "gpu_vendor"),
            ("GPU Product Name", "product_name"),
            ("PCI Device ID", "pci_device_id"),
            ("PCI Vendor ID", "pci_vendor_id"),
        ]

        left_column = QVBoxLayout()
        left_column.addSpacing(20)
        left_column.addLayout(self.build_pair_grid(vendor_rows))
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

        self.fan_duty.setText(f"{data.get('Fan Duty (%)') or 0:.0f}%")
        self.performarce.setText(str(data.get("Performance Mode")))
        self.temp_edge.setText(f"{data.get('Temperature Edge (°C)') or 0:.1f} °C")
        self.power_draw.setText(f"{data.get('Power Draw (W)') or 0:.1f} W")
        self.power_limit.setText(f"{data.get('Power Limit (W)') or 0:.0f} W")

        self.voltage.setText(f"{data.get('Voltage (mV)') or 0:.0f} mV")
        self.core_clock.setText(f"{data.get('Core Clock (MHz)') or 0:.0f} MHz")
        self.memory_clock.setText(f"{data.get('Memory Clock (MHz)') or 0:.0f} MHz")
        self.fan_speed.setText(f"{data.get('Fan Speed (RPM)') or 0:.0f} RPM")

        self.gpu_data.append(gpu_percent)
        self.gpu_curve.setData(list(self.gpu_data))
        self.gpu_label.setText(f'GPU: {gpu_percent}')
    
    def get_static(self, data):
        self.vbios_version.setText(str(data.get("VBIOS")))
        self.vram_total_mib.setText(str(data.get("VRAM")))
        self.gtt.setText(str(data.get("GTT")))
        self.perf.setText(str(data.get("Perf level")))

        self.cap_max.setText(str(data.get("Power cap max")))
        self.cap_def.setText(str(data.get("Power cap def")))

        self.temp_critical_c.setText(f"{data.get('Temperature Critical (°C)') or 0:.0f} °C")
        self.temp_emergency_c.setText(f"{data.get('Temperature Emergency (°C)') or 0:.0f} °C")

        self.fan_rpm_min.setText(f"{data.get('Fan RPM Min') or 0:.0f} RPM")
        self.fan_rpm_max.setText(f"{data.get('Fan RPM Max') or 0:.0f} RPM")
    
    def get_vendor(self, data):
        self.gpu_model.setText(str(data.get("GPU")))
        self.gpu_vendor.setText(str(data.get("Vendor")))
        self.pci_device_id.setText(str(data.get("PCI Device ID")))
        self.pci_vendor_id.setText(str(data.get("PCI Vendor ID")))

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
        




