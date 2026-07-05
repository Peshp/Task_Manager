import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

from ui.main_window import MainWindow


app = QApplication(sys.argv)

window = MainWindow()

window.show()
sys.exit(app.exec())