from PyQt6.QtCore import Qt, QEvent, QCoreApplication
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QTabWidget
)
from widgets.title_bar import TitleBar
from tabs.performarce_tab import PerformarceTab
from tabs.processes_tab import ProcessesTab
from tabs.memory_tab import MemoryTab
from tabs.disk_tab import DiskTab
from tabs.cpu_tab import CPUTab
from tabs.gpu_tab import GPUTab
from tabs.network_tab import NetworkTab
from monitors.system_monitor import SystemMonitor
from monitors.memory_monitor import MemoryMonitor
from monitors.cpu_monitor import CPUMonitor
from monitors.network_monitor import NetworkMonitor
from monitors.processes_monitor import ProcessesMonitor
from monitors.disk_monitor import DiskMonitor
from monitors.gpu_monitor import GPUMonitor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manager")
        self.setMouseTracking(True)
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
        self.cpu_monitor = CPUMonitor(interval_ms=1000)
        self.net_monitor = NetworkMonitor(interval_ms=1000)
        self.proc_monitor = ProcessesMonitor(interval_ms=1000)
        self.disk_monitor = DiskMonitor(interval_ms=1000)
        self.gpu_monitor = GPUMonitor(interval_ms=1000)

        self.processes_tab = ProcessesTab()
        self.performance_tab = PerformarceTab()
        self.memory_tab = MemoryTab()
        self.disk_tab = DiskTab()
        self.cpu_tab = CPUTab()
        self.net_tab = NetworkTab()
        self.gpu_tab = GPUTab()

        self.monitor.stats_updated.connect(self.performance_tab.update_data)
        self.net_monitor.stats_updated.connect(self.performance_tab.net_update_data)
        self.disk_monitor.stats_updated_disk.connect(self.performance_tab.disk_update_data)
        self.net_monitor.stats_updated.connect(self.net_tab.update_data)
        self.cpu_monitor.stats_updated.connect(self.cpu_tab.update_data)
        self.gpu_monitor.stats_updated.connect(self.gpu_tab.update_data)
        self.proc_monitor.stats_updated.connect(self.processes_tab.update_data)
        self.memory_monitor.stats_updated.connect(self.memory_tab.update_data)
        self.disk_monitor.stats_updated_disk.connect(self.disk_tab.update_data)
        self.cpu_tab.get_architecture(self.cpu_monitor.get_static())
        self.cpu_tab.get_vendor(self.cpu_monitor.get_static())
        self.cpu_tab.get_static(self.cpu_monitor.get_static())
        self.gpu_tab.get_static(self.gpu_monitor.get_static())
        self.gpu_tab.get_vendor(self.gpu_monitor.get_static())
        self.memory_tab.get_memory_stats(self.memory_monitor.get_mem_gb())
        self.performance_tab.set_cpu_name(self.monitor.get_cpu_name())
        self.disk_tab.set_disk_capacity(self.disk_monitor.get_disk_stats())
        self.net_tab.get_static(self.net_monitor.get_static())
        

        work_space_layout = QVBoxLayout()
        work_space_layout.setContentsMargins(20, 16, 20, 20)
        
        self.tabs = QTabWidget()
        self.tabs.addTab(self.processes_tab, 'Processes')
        self.tabs.addTab(self.performance_tab, 'Performance')
        self.tabs.addTab(self.cpu_tab, 'CPU')
        self.tabs.addTab(self.gpu_tab, 'GPU')
        self.tabs.addTab(self.memory_tab, 'RAM')
        self.tabs.addTab(self.disk_tab, 'Disk')
        self.tabs.addTab(self.net_tab, 'Network')

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

    def _edge_at(self, pos):
        rect = self.rect()
        edges = Qt.Edge(0)
        if pos.x() <= 8:
            edges |= Qt.Edge.LeftEdge
        elif pos.x() >= rect.width() - 8:
            edges |= Qt.Edge.RightEdge
        if pos.y() <= 8:
            edges |= Qt.Edge.TopEdge
        elif pos.y() >= rect.height() - 8:
            edges |= Qt.Edge.BottomEdge
        return edges

    def mouseMoveEvent(self, event):
        edges = self._edge_at(event.position().toPoint())
        cursors = {
            Qt.Edge.LeftEdge: Qt.CursorShape.SizeHorCursor,
            Qt.Edge.RightEdge: Qt.CursorShape.SizeHorCursor,
            Qt.Edge.TopEdge: Qt.CursorShape.SizeVerCursor,
            Qt.Edge.BottomEdge: Qt.CursorShape.SizeVerCursor,
            Qt.Edge.LeftEdge | Qt.Edge.TopEdge: Qt.CursorShape.SizeFDiagCursor,
            Qt.Edge.RightEdge | Qt.Edge.BottomEdge: Qt.CursorShape.SizeFDiagCursor,
            Qt.Edge.RightEdge | Qt.Edge.TopEdge: Qt.CursorShape.SizeBDiagCursor,
            Qt.Edge.LeftEdge | Qt.Edge.BottomEdge: Qt.CursorShape.SizeBDiagCursor,
        }
        self.setCursor(cursors.get(edges, Qt.CursorShape.ArrowCursor))
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            edges = self._edge_at(event.position().toPoint())
            if edges != Qt.Edge(0):
                self.windowHandle().startSystemResize(edges)
                return
        super().mousePressEvent(event)
    
    
