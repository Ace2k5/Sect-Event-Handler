from frontend import init_window
import sys
from PySide6.QtWidgets import QApplication



app = QApplication(sys.argv)
init_window = init_window.Window()
init_window.show()
app.exec()