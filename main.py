from frontend import main_window
import sys
from PySide6.QtWidgets import QApplication



app = QApplication(sys.argv)
main_window = main_window.Window()
main_window.show()
app.exec()