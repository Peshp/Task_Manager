from PyQt6.QtCore import Qt, QEvent, QPoint
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel
)

from ui.widgets.title_bar import TitleBar

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

        work_space_layout = QVBoxLayout()
        work_space_layout.setContentsMargins(20, 16, 20, 20)
        hello_label = QLabel("Hello, World!", self)
        hello_label.setStyleSheet("color: white;")
        work_space_layout.addWidget(hello_label)

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
    
    
