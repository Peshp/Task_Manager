import pyqtgraph as pg
from collections import deque
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout

class GPUTab(QWidget):
    MAX_POINTS = 60

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        self.gpu_data = deque([0] * self.MAX_POINTS, maxlen=self.MAX_POINTS)

        # ---- Header ----
        gpu_header = QHBoxLayout()
        self.gpu_label = QLabel("GPU")
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

        bottom_container = QHBoxLayout()
        bottom_container.setSpacing(20)

        # ---------- LEFT MAIN COLUMN (dynamic) ----------
        left_main = QVBoxLayout()
        left_main.setSpacing(5)

        dynamic_grid = QHBoxLayout()
        dynamic_grid.setSpacing(10)

        dyn_col1 = QVBoxLayout()
        dyn_col1.setSpacing(4)

        self.gpuload_title = QLabel("GPU load:")
        self.gpuload_title.setStyleSheet("color: #9b9b9b; font-size: 14pt;")
        self.gpuload = QLabel("0%")
        self.gpuload.setStyleSheet("color: white; font-size: 22pt; font-weight: 300;")
        dyn_col1.addWidget(self.gpuload_title)
        dyn_col1.addWidget(self.gpuload )
        dyn_col1.addSpacing(10)

        # self.processes_title = QLabel("Processes")
        # self.processes_title.setStyleSheet("color: #9b9b9b; font-size: 14pt;")
        # self.processes = QLabel("0")
        # self.processes.setStyleSheet("color: white; font-size: 16pt;")
        # dyn_col1.addWidget(self.processes_title)
        # dyn_col1.addWidget(self.processes)
        # dyn_col1.addSpacing(10)

        self.pci_max_speed_title = QLabel("CPU Load (%)")
        self.pci_max_speed_title.setStyleSheet("color: #9b9b9b; font-size: 14pt;")
        self.pci_max_speed = QLabel("00:00:00")
        self.pci_max_speed.setStyleSheet("color: white; font-size: 16pt;")
        dyn_col1.addWidget(self.pci_max_speed_title)
        dyn_col1.addWidget(self.pci_max_speed)
        dyn_col1.addStretch()

        dyn_col2 = QVBoxLayout()
        dyn_col2.setSpacing(4)   

        # self.speed_title = QLabel("Speed")
        # self.speed_title.setStyleSheet("color: #9b9b9b; font-size: 14pt;")
        # self.current_speed = QLabel("0.00 GHz")
        # self.current_speed.setStyleSheet("color: white; font-size: 22pt; font-weight: 300;")
        # dyn_col2.addWidget(self.speed_title)
        # dyn_col2.addWidget(self.current_speed)
        # dyn_col2.addSpacing(10)

        # self.threads_title = QLabel("Threads")
        # self.threads_title.setStyleSheet("color: #9b9b9b; font-size: 14pt;")
        # self.threads = QLabel("0")
        # self.threads.setStyleSheet("color: white; font-size: 22pt;")
        # dyn_col2.addWidget(self.threads_title)
        # dyn_col2.addWidget(self.threads)
        # dyn_col2.addSpacing(10)

        dynamic_grid.addLayout(dyn_col1)
        dynamic_grid.addLayout(dyn_col2)

        left_main.addLayout(dynamic_grid)
        left_main.addStretch()

        # ---------- RIGHT MAIN COLUMN (dynamic) ----------
        right_main = QGridLayout()
        right_main.setHorizontalSpacing(50)
        right_main.setVerticalSpacing(0)

        static_rows = [
            ("GPU Load (%):", "gpu_load"),
        ]

        # architecture = [
        #     ("Architecture:", "architecture_val"),
        #     ("CPU op-mode(s):", "op_modes"),
        #     ("Address sizes:", "address_sizes"),
        # ]

        vendor = [
            ("GPU family:", "AMD"),
        ]

        left_column = QVBoxLayout()
        # left_column.addLayout(self.build_pair_grid(architecture))
        left_column.addSpacing(20)
        left_column.addLayout(self.build_pair_grid(vendor))
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

        self.gpuload.setText(f'{gpu_percent:.0f}%')
        print(data)

        self.gpu_data.append(gpu_percent)
    
    def get_static(self, data):
        pci_max_speed = data['Temperature Critical (°C)']
        self.pci_max_speed.setText(str(pci_max_speed))

    def get_architecture(self, data):
        architecture_val = data.get('Architecture', 'N/A')
        op_modes = data.get('CPU op-mode(s)', 'N/A')
        address_sizes = data.get('Address sizes', 'N/A')

        self.architecture_val.setText(architecture_val)
        self.op_modes.setText(op_modes)
        self.address_sizes.setText(address_sizes)
    
    def get_vendor(self, data):
        cpu_family = data.get('CPU family', 'N/A')
        cpu_model = data.get('Model', 'N/A')
        threads_per_core = data.get('Thread(s) per core', 'N/A')
        cores_per_socket = data.get('Core(s) per socket', 'N/A')
        cpu_max_mhz = data.get('CPU max MHz', 'N/A')
        cpu_min_mhz = data.get('CPU min MHz', 'N/A')

        self.cpu_family.setText(cpu_family)
        self.cpu_model.setText(cpu_model)
        self.threads_per_core.setText(threads_per_core)
        self.cores_per_socket.setText(cores_per_socket)
        self.cpu_max_mhz.setText(cpu_max_mhz)
        self.cpu_min_mhz.setText(cpu_min_mhz)

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
        




