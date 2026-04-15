from frontend import main_window
import sys
from PySide6.QtWidgets import QApplication
from backend import flow

app = QApplication(sys.argv)
main = main_window.Window()
scraper = flow.ScrapeFlow(signals=main.log_signal)
main.setup(run=scraper.flow, save=scraper.save_data)
main.show()
app.exec()