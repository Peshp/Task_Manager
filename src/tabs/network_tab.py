import pyqtgraph as pg
from collections import deque
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout
from widgets.tab_service import make_stat_column, build_pair_grid

class NetworkTab(QWidget):
    MAX_POINTS = 60

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        self.net_data_download = deque([0.0] * self.MAX_POINTS, maxlen=self.MAX_POINTS)
        self.net_data_upload = deque([0.0] * self.MAX_POINTS, maxlen=self.MAX_POINTS)

        net_header = QHBoxLayout()
        self.net_label = QLabel("")
        self.net_label.setStyleSheet("color: white; font-size: 14pt; font-weight: 600;")

        net_header.addWidget(self.net_label)
        layout.addLayout(net_header)

        self.net_plot = pg.PlotWidget()
        self.net_plot.setBackground("#1e1e1e")
        self.net_plot.setYRange(0, 100)
        self.net_plot.showGrid(x=True, y=True, alpha=0.2)

        self.net_curve_download = self.net_plot.plot(
            list(self.net_data_download), pen=pg.mkPen(color="#9B59B6", width=2)
        )
        self.net_curve_upload = self.net_plot.plot(
            list(self.net_data_upload), pen=pg.mkPen(color="#F1C40F", width=2)
        )
        layout.addWidget(self.net_plot)

        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(50)
        bottom_row.setContentsMargins(0, 20, 0, 0)

        dyn_col1 = make_stat_column(self, [("Download", "download"), ("Upload", "upload")])
        bottom_row.addLayout(dyn_col1)

        static_rows = [
            ("IPv4:", "ipv4"),
            ("IPv6:", "ipv6"),
            ("Connection Type:", "connection_type"),
            ("Version:", "version")
        ]
        static_col = QVBoxLayout()
        static_col.setContentsMargins(0, 0, 0, 0)
        static_col.addLayout(build_pair_grid(self, static_rows))
        static_col.addStretch(1)

        bottom_row.addLayout(static_col)
        bottom_row.addStretch(1)

        layout.addLayout(bottom_row)

    def update_data(self, data):
        download_mbps = data['download_mbps']
        upload_mbps = data['upload_mbps']

        self.download_value.setText(f"{download_mbps:.2f} Mbps")
        self.upload_value.setText(f"{upload_mbps:.2f} Mbps")

        self.net_data_download.append(download_mbps)
        self.net_data_upload.append(upload_mbps)

        self.net_curve_download.setData(list(self.net_data_download))
        self.net_curve_upload.setData(list(self.net_data_upload))

    def get_static(self, data):
        for key, val in data.items():
            if key == 'ipv4':
                self.ipv4.setText(data['ipv4'])
            elif key == 'ipv6':
                self.ipv6.setText(data['ipv6'])
        self.connection_type.setText(data['connection_type'])
        self.version.setText(data['version'])

        self.net_label.setText(data['connection_type'])