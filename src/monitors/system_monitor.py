import psutil
from PyQt6.QtCore import QObject, QTimer, pyqtSignal

class SystemMonitor(QObject):
    stats_updated = pyqtSignal(dict)

    def __init__(self, interval_ms=1000, parent=None):
        super().__init__(parent)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.poll)
        self.timer.start(interval_ms)

        self.cpu_name = self.get_cpu_name()
        self.memory_capacity = self.get_mem_gb()
    
    def poll(self):
        data = {
            'cpu': psutil.cpu_percent(),
            'memory': psutil.virtual_memory(),
            'processes': list(psutil.process_iter(
                ['pid', 'name', 'cpu_percent', 'memory_percent']
            )),
        }
        self.stats_updated.emit(data)
    
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

        return f"Total: {total_gb:.1f}GB    Used: {active_gb:.1f}GB    Avalaibe: {free_gb:.1f}GB"
