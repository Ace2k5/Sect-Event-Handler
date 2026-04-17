from frontend import main_window
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from backend import flow
import removal

app = QApplication(sys.argv)
main = main_window.Window()
scraper = flow.ScrapeFlow(signals=main.log_signal)
main.setup(run=scraper.flow, save_game=scraper.save_data_game, save_settings=scraper.save_data_settings)
main.show()
removal.remove_min_max(int(main.winId()))
app.exec()