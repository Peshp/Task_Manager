import psutil
import subprocess
import time
from PyQt6.QtCore import QObject, QTimer, pyqtSignal

class MemoryMonitor(QObject):
    stats_updated = pyqtSignal(dict)

    def __init__(self, interval_ms=1000, parent=None):
        super().__init__(parent)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.poll)
        self.timer.start(interval_ms)

        self.memory_capacity = self.get_mem_gb()
    
    def poll(self):
        vm = psutil.virtual_memory()
        data = {
            'memory': vm,
            'active': vm.used / (1024**3),
            'free': vm.available / (1024**3),
            'cached': (vm.cached / (1024**3)) + (vm.buffers / (1024**3)),
            'shared': vm.shared / (1024**3) 
        }
        self.stats_updated.emit(data)
    
    def get_mem_gb(self):      
        result = subprocess.run(
            ['sudo', 'dmidecode', '--type', 'memory'],
            capture_output=True, text=True
        )

        stats = {}

        for i in result.stdout.splitlines():
            splitted = i.strip()
            if ':' in splitted:
                key, _, value = splitted.partition(':')
                key = key.strip()
                value = value.strip()
                stats[key] = value 
        
        return stats
        
    

