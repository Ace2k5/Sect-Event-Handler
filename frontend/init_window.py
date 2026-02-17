import sys
from PySide6.QtCore import Qt, QThreadPool
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                                QHBoxLayout, QPushButton, QTextEdit,
                                QSizePolicy)
from . import settings, worker
from backend import flow

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.pool = QThreadPool()
        self._init_window_settings()
        
    def _init_window_settings(self):
        layout = QHBoxLayout(self)
        vbox1 = QVBoxLayout()
        vbox2 = QVBoxLayout()


        window_title = settings.window_settings['window_name']
        w, h = settings.window_settings['resolution']
        
        self.setWindowTitle(window_title)
        self.resize(w, h)
        
        self._set_stylesheet()
        self._set_up_buttons(vbox1, vbox2)

        layout.addLayout(vbox1, 2)
        layout.addLayout(vbox2, 3)

    def test(self):
        def job(signals):
            runner = flow.ScrapeFlow(signals)
            runner.flow(forced=True)
        
        work = worker.Worker(job)

        work.signals.log.connect(self.log_menu.append)
        self.pool.start(work)

    def _set_up_buttons(self, vbox1, vbox2):
        self.event_button = QPushButton()
        self.webhook_button = QPushButton()
        self.event_button.setText("Force Send Events")
        self.webhook_button.setText("Manage Webhooks")

        self.event_button.setFixedHeight(50)
        self.webhook_button.setFixedHeight(50)
        
        self.log_menu = QTextEdit()
        self.log_menu.setReadOnly(True)
        self.log_menu.setMinimumWidth(100)
        self.log_menu.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        vbox1.addWidget(self.event_button)
        vbox1.addWidget(self.webhook_button)
        vbox1.addStretch()
        vbox2.addWidget(self.log_menu)
        self.event_button.clicked.connect(lambda: self.test())

    def _set_stylesheet(self):
        self.setStyleSheet('''
                        QWidget {
                            background-color: #1b1b1f;
                            color: white;
                        }
                            
                        QPushButton {
                            color: white;
                            font-size: 12px;
                            background-color: #141417;
                        }
                           
                        QTextEdit {
                           background-color: #141417;
                           }
                        ''')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()