from frontend import window
import sys
from PySide6.QtWidgets import QApplication



app = QApplication(sys.argv)
window = window.Window()
window.show()
app.exec()