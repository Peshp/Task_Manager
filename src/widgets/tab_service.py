import pyqtgraph as pg
from collections import deque
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QGridLayout

def make_stat_column(self, pairs):
    col = QVBoxLayout()
    col.setSpacing(0)
    col.setContentsMargins(0, 0, 0, 0)
    for title, attr in pairs:
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #9b9b9b; font-size: 14pt;")
        value_label = QLabel("")
        value_label.setStyleSheet("color: white; font-size: 22pt; font-weight: 300;")
        setattr(self, f"{attr}_title", title_label)
        setattr(self, f"{attr}_value", value_label)
        col.addWidget(title_label)
        col.addWidget(value_label)
        col.addSpacing(20)   
    col.addStretch(1)        
    return col

def build_pair_grid(self, pairs):
    grid = QGridLayout()
    grid.setHorizontalSpacing(15)
    grid.setVerticalSpacing(6)
    for row, (label_text, attr_name) in enumerate(pairs):
        key_label = QLabel(label_text)
        key_label.setStyleSheet("color: #9b9b9b; font-size: 13pt;")

        value_label = QLabel("-")
        value_label.setStyleSheet("color: white; font-size: 13pt;")

        setattr(self, attr_name, value_label)

        grid.addWidget(key_label, row, 0)
        grid.addWidget(value_label, row, 1)
    grid.setColumnStretch(1, 1)
    return grid

        