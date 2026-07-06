from PyQt6.QtWidgets import QLabel, QVBoxLayout

from ui.base_window import BaseWindow

class Memory(BaseWindow):
    def __init__(self):
        super().__init__()

        self.resize(700, 600)
        self.setWindowTitle(BaseWindow('RAM'))

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel('Memory')
        self.layout.addWidget(self.label)


