from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt

from ui.widgets.title_bar import TitleBar

class BaseWindow(QMainWindow):
    def __init__(self, title: str):
        super().__init__()

        self.setWindowTitle(title)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
        )

        self.title_bar = TitleBar(title)
        self.content = QWidget

        layout = QVBoxLayout

        layout.addWidget(self.title_bar)
        layout.addWidget(self.content)

        self.setLayout(layout)