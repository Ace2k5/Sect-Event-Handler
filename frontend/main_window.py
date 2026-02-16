from . import init_window
from ..backend import flow
import sys
from PySide6.QtWidgets import QApplication

app = QApplication(sys.argv)
window = init_window.Window()
window.show()
app.exec()