from frontend import init_window
import sys
from PySide6.QtWidgets import QApplication

app = QApplication(sys.argv)
window = init_window.Window()
window.show()
app.exec()