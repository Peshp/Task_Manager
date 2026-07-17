from PyQt6.QtCore import Qt, QEvent, QPoint
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QTabWidget
)
from widgets.title_bar import TitleBar
from tabs.performarce_tab import PerformarceTab
from tabs.processes_tab import ProcessesTab
from tabs.memory_tab import MemoryTab
from tabs.disk_tab import DiskTab
from monitors.system_monitor import SystemMonitor
from monitors.memory_monitor import MemoryMonitor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manager")
        self.resize(720, 584)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        central_widget = QWidget()
        central_widget.setObjectName("Container")
        central_widget.setStyleSheet(
            """#Container {
                    background: #191919;
                    border-radius: 5px;
                }
            """
        )
        self.title_bar = TitleBar(self)

        self.monitor = SystemMonitor(interval_ms=1000)
        self.memory_monitor = MemoryMonitor(interval_ms=1000)

        self.processes_tab = ProcessesTab()
        self.performance_tab = PerformarceTab()
        self.memory_tab = MemoryTab()
        self.disk_tab = DiskTab()

        self.monitor.stats_updated.connect(self.processes_tab.update_data)
        self.monitor.stats_updated.connect(self.performance_tab.update_data)
        self.memory_monitor.stats_updated.connect(self.memory_tab.update_data)
        self.monitor.stats_updated_disk.connect(self.disk_tab.update_data)
        self.memory_tab.get_memory_stats(self.memory_monitor.get_mem_gb())
        self.performance_tab.set_cpu_name(self.monitor.get_cpu_name())
        self.disk_tab.set_disk_capacity(self.monitor.get_disk_stats())

        work_space_layout = QVBoxLayout()
        work_space_layout.setContentsMargins(20, 16, 20, 20)
        
        self.tabs = QTabWidget()
        self.tabs.addTab(self.processes_tab, 'Processes')
        self.tabs.addTab(self.performance_tab, 'Performance')
        self.tabs.addTab(self.memory_tab, 'RAM')
        self.tabs.addTab(self.disk_tab, 'Disk')

        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: none; background: transparent; }
            QTabBar::tab {
                background: transparent;
                color: #cccccc;
                padding: 8px 16px;
            }
            QTabBar::tab:selected {
                color: white;
                border-bottom: 2px solid #4A90D9;
            }
        """)
        
        work_space_layout.addWidget(self.tabs)

        centra_widget_layout = QVBoxLayout()
        centra_widget_layout.setContentsMargins(0, 0, 0, 0)
        centra_widget_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        centra_widget_layout.addWidget(self.title_bar)
        centra_widget_layout.addLayout(work_space_layout)

        central_widget.setLayout(centra_widget_layout)
        self.setCentralWidget(central_widget)

    def changeEvent(self, event):
        if event.type() == QEvent.Type.WindowStateChange:
            self.title_bar.window_state_changed(self.windowState())
        super().changeEvent(event)
        event.accept()
    
    
