import os
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import QCoreApplication, Qt


class DarkTheme:
    @staticmethod
    def apply(app):
        QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, True)

        app.setStyle("Fusion")
        app.setPalette(DarkTheme._build_palette())
        app.setStyleSheet(DarkTheme._load_stylesheet())

    @staticmethod
    def _build_palette():
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(43, 43, 43))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(224, 224, 224))
        palette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 35))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(45, 45, 45))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(224, 224, 224))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(224, 224, 224))
        palette.setColor(QPalette.ColorRole.Text, QColor(224, 224, 224))
        palette.setColor(QPalette.ColorRole.Button, QColor(58, 58, 58))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(224, 224, 224))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.ColorRole.Link, QColor(90, 155, 212))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(217, 83, 30))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))

        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor(120, 120, 120))
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor(120, 120, 120))
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor(120, 120, 120))
        return palette

    @staticmethod
    def _load_stylesheet():
        qss_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.qss")
        try:
            with open(qss_path, "r", encoding="utf-8") as f:
                return f.read()
        except:
            pass