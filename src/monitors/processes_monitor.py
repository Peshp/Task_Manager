import psutil, time
from PyQt6.QtCore import QObject, QTimer, pyqtSignal

class ProcessesMonitor(QObject):
    stats_updated = pyqtSignal(list)

    def __init__(self, interval_ms=1000, parent=None):
        super().__init__(parent)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.poll)
        self.timer.start(interval_ms)

    def poll(self, limit=100):
        proc = []
        for pid in psutil.pids()[-200:]:
            try:
                p = psutil.Process(pid)
                p.cpu_percent()  
                proc.append(p)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        time.sleep(0.1)

        top = {}
        for p in proc:
            try:
                top[p] = p.cpu_percent() / psutil.cpu_count()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        top_list = sorted(top.items(), key=lambda x: x[1])
        top_n = top_list[-limit:]
        top_n.reverse()

        cpu_rows = []
        for p, cpu_percent in top_n:
            try:
                with p.oneshot():
                    cpu_rows.append({
                        'Path': p.exe(),
                        'PID': p.pid,
                        'Name': p.name(),
                        'Status': p.status(),
                        'CPU%': round(cpu_percent, 2),          
                        'Threads': p.num_threads(),              
                        'Mem(MB)': round(p.memory_info().rss / 1e6, 2)  
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        return self.stats_updated.emit(cpu_rows)