import psutil
import time
from PyQt6.QtCore import QObject, QTimer, pyqtSignal

class SystemMonitor(QObject):
    stats_updated = pyqtSignal(dict)
    stats_updated_disk = pyqtSignal(dict)

    def __init__(self, interval_ms=1000, parent=None):
        super().__init__(parent)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.poll)
        self.timer.start(interval_ms)

        self.disk_timer = QTimer(self)
        self.disk_timer.timeout.connect(self.poll_disk)
        self.disk_timer.start(interval_ms)

        self.cpu_name = self.get_cpu_name()

        self.disk_prev = psutil.disk_io_counters()
        self.disk_prev_time = time.time()

        self.disk_stats = self.get_disk_stats()
    
    def poll(self):
        data = {
            'cpu': psutil.cpu_percent(),
            'memory': psutil.virtual_memory(),
            'processes': list(psutil.process_iter(
                ['pid', 'name', 'cpu_percent', 'memory_percent']
            )),

        }
        self.stats_updated.emit(data)
    
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
    
    def get_cpu_name(self):
        with open("/proc/cpuinfo") as f:
            for line in f:
                if line.strip().startswith("model name"):
                    return line.split(":", 1)[1].strip()
        return "Unknown CPU"
    
    def get_mem_gb(self):
        mem = psutil.virtual_memory()
        total_gb = mem.total / (1024 ** 3)
        active_gb = mem.used / (1024 ** 3)
        free_gb = mem.available / (1024 ** 3)
        cached_gb = mem.cached / (1024 ** 3)
        buffers_gb = mem.buffers / (1024 ** 3)
        shared_gb = mem.shared / (1024 ** 3)

        return f"Total: {total_gb:.1f}GB    Used: {active_gb:.1f}GB    Avalaibe: {free_gb:.1f}GB \
                Cached: {cached_gb:.2f}  Buffers {buffers_gb:.2f}  Shared: {shared_gb:.2f}"
    

