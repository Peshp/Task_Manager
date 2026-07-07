from PyQt6.QtWidgets import QTabWidget, QWidget, QVBoxLayout

class ProcessesTab(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
    
    def update_data(self, data):
        for proc in data['processes']:
            print(proc)

