import psutil
import subprocess
import time
import glob
import os
import numpy
from datetime import timedelta
from PyQt6.QtCore import QObject, QTimer, pyqtSignal

class GPUMonitor(QObject):
    stats_updated = pyqtSignal(dict)

    def __init__(self, interval_ms=1000, parent=None):
        super().__init__(parent)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.poll)
        self.timer.start(interval_ms)

        self.D = "/sys/devices/pci0000:00/0000:00:01.1/0000:10:00.0"
        self.H = "/sys/class/hwmon/hwmon0"

        self.data = self.get_static()
    
    def poll(self):
        pwm = self.number(f"{self.H}/pwm1", 1, 0)
        data = {
            "GPU Load (%)": self.number(f"{self.D}/gpu_busy_percent", 1, 0),
            "Fan Duty (%)": None if pwm is None else round(pwm / 255 * 100, 1),
        }
        self.stats_updated.emit(data)

    def text(self, path):
        try:
            with open(path) as f:
                return f.read().strip()
        except OSError:
            return None
    
    def number(self, path, divide=1, digits=2):
        t = self.text(path)
        try:
            return round(float(t.split()[0]) / divide, digits)
        except (AttributeError, IndexError, ValueError):
            print(t)
    
    def get_static(self):    
        data = {
            "Temperature Critical (°C)": self.number(f"{self.H}/temp1_crit", 1000, 1)
        }
        
        return data

         