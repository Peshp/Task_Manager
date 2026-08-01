import psutil
import time
from PyQt6.QtCore import QObject, QTimer, pyqtSignal

class DiskMonitor(QObject):
    stats_updated_disk = pyqtSignal(dict)

    def __init__(self, interval_ms=1000, parent=None):
        super().__init__(parent)
        self.disk_timer = QTimer(self)
        self.disk_timer.timeout.connect(self.poll_disk)
        self.disk_timer.start(interval_ms)

        self.disk_prev = psutil.disk_io_counters()
        self.disk_prev_time = time.time()

        self.disk_stats = self.get_disk_stats()
    
    def poll_disk(self):
        disk_now = psutil.disk_io_counters()
        now = time.time()
        elapsed = now - self.disk_prev_time

        read_speed = (disk_now.read_bytes - self.disk_prev.read_bytes) / (1024 ** 2) / elapsed
        write_speed = (disk_now.write_bytes - self.disk_prev.write_bytes) / (1024**2) / elapsed if elapsed > 0 else 0

        busy_ms_this_interval = disk_now.busy_time - self.disk_prev.busy_time
        active_pct = (busy_ms_this_interval / (elapsed * 1000)) * 100

        time_delta = (disk_now.read_time - self.disk_prev.read_time) + \
                        (disk_now.write_time - self.disk_prev.write_time)
        count_delta = (disk_now.read_count - self.disk_prev.read_count) + \
                        (disk_now.write_count - self.disk_prev.write_count)

        if count_delta > 0:
            avg_responses = time_delta / count_delta
        else:
            avg_responses = 0
        
        data = {
            'active': active_pct,
            'read': read_speed,
            'write': write_speed,
            'avg_responses': avg_responses,
        }

        self.stats_updated_disk.emit(data)

        self.disk_prev = disk_now
        self.disk_prev_time = now

    def get_disk_stats(self):
        disk = psutil.disk_usage('/')

        data = {
            'total': disk.total / (1024**3),
            'used': disk.used / (1024**3),
            'free': disk.free / (1024**3),
        }

        return data