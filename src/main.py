import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt, QCoreApplication

from main_window import MainWindow
from theme import DarkTheme


app = QApplication(sys.argv)
DarkTheme.apply(app)

window = MainWindow()

window.show()
sys.exit(app.exec())