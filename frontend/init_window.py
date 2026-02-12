import sys
from PySide6.QtWidgets import QMainWindow, QApplication

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Event Handler | 0.001")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()