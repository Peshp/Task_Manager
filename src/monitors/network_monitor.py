import psutil, time, socket
import subprocess
from PyQt6.QtCore import QObject, QTimer, pyqtSignal

class NetworkMonitor(QObject):
    stats_updated = pyqtSignal(dict)

    def __init__(self, interval_ms=1000, parent=None):
        super().__init__(parent)
        self.interval_s = interval_ms / 1000.0
        self.last = psutil.net_io_counters(pernic=True).get('wlo1')
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.poll)
        self.timer.start(interval_ms)

        self.data = self.get_static()

    def get_uevent_info(self, interface_name):
        result = subprocess.run(
            ["ethtool", "-i", interface_name],
            capture_output=True, text=True
        )
        info = {}
        for line in result.stdout.splitlines():
            if ":" in line:
                key, val = line.split(":", 1)
                info[key.strip()] = val.strip()
        return info

    def poll(self):
        counters = psutil.net_io_counters(pernic=True)
        new = counters.get('wlo1')
        if new is None or self.last is None:
            self.last = new
            return

        sent_bytes = new.bytes_sent - self.last.bytes_sent
        recv_bytes = new.bytes_recv - self.last.bytes_recv
        self.last = new

        data = {
            'upload_mbps': (sent_bytes * 8) / (self.interval_s * 1_000_000),
            'download_mbps': (recv_bytes * 8) / (self.interval_s * 1_000_000),
        }
        self.stats_updated.emit(data)

    def find_ethernet_interface(self):
        for name in psutil.net_if_addrs():
            if name.startswith("en"):
                return name
        return None

    def find_wifi_interface(self):
        for name in psutil.net_if_addrs():
            if name.startswith("wl"):
                return name
        return None

    def get_static(self):
        data = dict()

        wifi = self.find_wifi_interface() 
        eth = self.find_ethernet_interface()

        data['connection_type'] = 'Wi-Fi' if wifi != None else 'Ethernet'
        iface = wifi if wifi != None else eth
        info = self.get_uevent_info(iface)

        addrs = psutil.net_if_addrs()[iface]
        ipv4 = ipv6 = None
        for addr in addrs:
            if addr.family == socket.AF_INET:
                data['ipv4'] = addr.address
            elif addr.family == socket.AF_INET6:
                data['ipv6'] = addr.address.split('%')[0]

        for key, val in info.items():
            if key in ('version', 'bus-info'):
                data[key] = val

        return data

