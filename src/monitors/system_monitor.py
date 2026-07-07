import psutil
from PyQt6.QtCore import QObject, QTimer, pyqtSignal

class SystemMonitor(QObject):
    stats_updated = pyqtSignal(dict)

    def __init__(self, interval_ms=1000, parent=None):
        super().__init__(parent)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.poll)
        self.timer.start(interval_ms)
    
    def poll(self):
        data = {
            'cpu': psutil.cpu_percent(),
            'memory': psutil.virtual_memory(),
            'processes': list(psutil.process_iter(
                ['pid', 'name', 'cpu_percent', 'memory_percent']
            )),
        }
        self.stats_updated.emit(data)
