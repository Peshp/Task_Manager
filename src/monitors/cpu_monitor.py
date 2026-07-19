import psutil
import subprocess
import time
import numpy
from datetime import timedelta
from PyQt6.QtCore import QObject, QTimer, pyqtSignal

class CPUMonitor(QObject):
    stats_updated = pyqtSignal(dict)

    def __init__(self, interval_ms=1000, parent=None):
        super().__init__(parent)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.poll)
        self.timer.start(interval_ms)

        self.data = self.get_static()
    
    def poll(self):
        data = {
            'utilization': psutil.cpu_percent(),
            'current_speed': psutil.cpu_freq().current / 1000,
            'processes': len(psutil.pids()),
            'threads': len(list(psutil.process_iter(['num_threads'])))
        }

        self.stats_updated.emit(data)
    
    def get_static(self):    
        data = {
            'uptime': str(timedelta(seconds=int(time.time() - psutil.boot_time()))),
            'psyhical': psutil.cpu_count(logical=False),
            'logical': psutil.cpu_count(logical=True),
        }

        result = subprocess.run(
            ['lscpu'],
            capture_output=True, text=True
        )
        for i in result.stdout.splitlines():
            if ":" in i:
                label, value = i.split(':', 1)
                data[label.strip()] = value.strip()
        
        return data
         