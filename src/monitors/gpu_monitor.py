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
            "Performance Mode": self.text(f"{self.D}/power_dpm_force_performance_level"),
            "Temperature Edge (°C)": self.number(f"{self.H}/temp1_input", 1000, 1),
            "Power Draw (W)": self.number(f"{self.H}/power1_average", 1e6),
            "Power Limit (W)": self.number(f"{self.H}/power1_cap", 1e6),
            "Voltage (mV)": self.number(f"{self.H}/in0_input", 1, 0),
            "Core Clock (MHz)": self.number(f"{self.H}/freq1_input", 1e6, 0),
            "Memory Clock (MHz)": self.number(f"{self.H}/freq2_input", 1e6, 0),
            "Fan Speed (RPM)": self.number(f"{self.H}/fan1_input", 1, 0)
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
            pass

    def run(self, cmd):
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return r.stdout.strip() or "n/a"
    
    def get_static(self):    
        DEV = "/sys/class/drm/card1/device"

        vendor     = self.run(f"cat {DEV}/vendor")
        device     = self.run(f"cat {DEV}/device")
        revision   = self.run(f"cat {DEV}/revision")
        vram       = self.run(f"cat {DEV}/mem_info_vram_total")
        gtt        = self.run(f"cat {DEV}/mem_info_gtt_total")
        perf       = self.run(f"cat {DEV}/power_dpm_force_performance_level")
        cap_max    = self.run(f"cat {DEV}/hwmon/hwmon*/power1_cap_max")
        cap_def    = self.run(f"cat {DEV}/hwmon/hwmon*/power1_cap_default")
        vbios      = self.run(f"cat {DEV}/vbios_version")
        sclk       = self.run(f"cat {DEV}/pp_dpm_sclk")
        mclk       = self.run(f"cat {DEV}/pp_dpm_mclk")

        temp_crit  = self.run(f"cat {DEV}/hwmon/hwmon*/temp1_crit")
        temp_emerg = self.run(f"cat {DEV}/hwmon/hwmon*/temp1_emergency")
        fan_min    = self.run(f"cat {DEV}/hwmon/hwmon*/fan1_min")
        fan_max    = self.run(f"cat {DEV}/hwmon/hwmon*/fan1_max")

        vendor_name = {"0x1002": "AMD", "0x10de": "NVIDIA", "0x8086": "Intel"}.get(vendor, vendor)
        gpu_name = self.run(f"lspci -d {vendor[2:]}:{device[2:]} | cut -d: -f3-").strip()

        gib = lambda b: f"{int(b) / 1024**3:.2f} GiB"
        watt = lambda u: f"{int(u) / 1_000_000:.0f} W"
        num = lambda v, d=1: int(v) / d if v.lstrip("-").isdigit() else None   # new

        data = {
            "Vendor": f"{vendor_name} ({vendor})",
            "GPU": f"{gpu_name} ({device}, rev {revision})",
            "VRAM": gib(vram),
            "GTT": gib(gtt),
            "Perf level": perf,
            "Power cap max": watt(cap_max),
            "Power cap def": watt(cap_def),
            "VBIOS": vbios,
            "Core clocks": sclk.replace("*", "<-- current").splitlines(),
            "Memory clocks": mclk.replace("*", "<-- current").splitlines(),

            "Temperature Critical (°C)": num(temp_crit, 1000),
            "Temperature Emergency (°C)": num(temp_emerg, 1000),
            "Fan RPM Min": num(fan_min),
            "Fan RPM Max": num(fan_max),
        }
                
        return data
    
    def command(self, cmd, default="N/A"):
        try:
            out = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=5
            ).stdout.strip()
            return out or default
        except Exception:
            return default


         