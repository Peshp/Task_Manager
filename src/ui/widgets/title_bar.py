from PyQt6.QtCore import QEvent, QSize, Qt, QPoint
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QToolButton,
    QWidget,
    QStyle,
)

class TitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.main_window = parent
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.setFixedHeight(32)

        title_bar_layout = QHBoxLayout(self)
        title_bar_layout.setContentsMargins(1, 1, 1, 1)
        title_bar_layout.setSpacing(2)
        self.title = QLabel(f"{self.__class__.__name__}", self)
        self.title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.title.setStyleSheet(
            """QLabel {
                    text-transform: uppercase;
                    font-size: 15pt;
                    margin-left: 15px;
                    margin-top: 11px;
                    color: white;
                }
            """
        )

        if title := parent.windowTitle():
            self.title.setText(title)
        title_bar_layout.addWidget(self.title)

        # Min button
        self.min_button = QToolButton(self)
        min_icon = self.style().standardIcon(
            QStyle.StandardPixmap.SP_TitleBarMinButton,
        )
        self.min_button.setIcon(min_icon)
        self.min_button.clicked.connect(self.window().showMinimized)

        # Max button
        self.max_button = QToolButton(self)
        max_icon = self.style().standardIcon(
            QStyle.StandardPixmap.SP_TitleBarMaxButton,
        )
        self.max_button.setIcon(max_icon)
        self.max_button.clicked.connect(self.window().showMaximized)

        # Close button
        self.close_button = QToolButton(self)
        close_icon = self.style().standardIcon(
            QStyle.StandardPixmap.SP_TitleBarCloseButton
        )
        self.close_button.setIcon(close_icon)
        self.close_button.clicked.connect(self.window().close)

        # Normal button
        self.normal_button = QToolButton(self)
        normal_icon = self.style().standardIcon(
            QStyle.StandardPixmap.SP_TitleBarNormalButton
        )
        self.normal_button.setIcon(normal_icon)
        self.normal_button.clicked.connect(self.window().showNormal)
        self.normal_button.setVisible(False)
        # Add buttons
        buttons = [
            self.min_button,
            self.normal_button,
            self.max_button,
            self.close_button,
        ]
        for button in buttons:
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            button.setFixedSize(QSize(30, 30))
            button.setStyleSheet(
                """
                    QToolButton {
                        background-color: transparent;
                        color: #cccccc;
                        border: none;
                        font-family: "Segoe UI", sans-serif;
                        padding: 2px;
                    }
                    QToolButton:hover {
                        background-color: #4A90D9;
                    }
                    QToolButton:pressed {
                        background-color: #3A78BD;
                    }
                """
            )
            title_bar_layout.addWidget(button)

    def window_state_changed(self, state):
        if state == Qt.WindowState.WindowMaximized:
            self.normal_button.setVisible(True)
            self.max_button.setVisible(False)
        else:
            self.normal_button.setVisible(False)
            self.max_button.setVisible(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            window_handle = self.main_window.windowHandle()
            if window_handle is not None:
                window_handle.startSystemMove()
            event.accept()


    

