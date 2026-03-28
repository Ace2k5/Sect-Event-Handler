import sys
from PySide6.QtCore import Qt, QThreadPool, QTimer
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                                QHBoxLayout, QPushButton, QTextEdit,
                                QSizePolicy)
from . import settings, worker, webhook_subwindow
from backend import flow

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.runner = None
        self.pool = QThreadPool()
        self.window_settings()
        self._init_event_widgets()
        self._init_webhook_widgets()
        self.event_button.clicked.connect(lambda: QTimer.singleShot(300, self.worker_thread()))

    def switch_buttons(self, mode):
        if mode == "events":
            self.webhook.button.hide()
            self.log_menu.show()
        elif mode == "webhook":
            self.log_menu.hide()
            self.webhook.button.show()
        
    def window_settings(self):
        layout = QHBoxLayout(self)
        self.vbox1 = QVBoxLayout()
        self.vbox2 = QVBoxLayout()


        window_title = settings.window_settings['window_name']
        w, h = settings.window_settings['resolution']
        
        self.setWindowTitle(window_title)
        self.resize(w, h)
        
        self._set_stylesheet()
        self._set_up_buttons()

        layout.addLayout(self.vbox1, 2)
        layout.addLayout(self.vbox2, 3)

    # Worker thread for backend.
    def job(self, signals):
        if self.runner is None:   
            self.runner = flow.ScrapeFlow(signals)
            self.runner.flow(forced=True)
        else:
            self.runner.flow(forced=True)

    def worker_thread(self):
        work = worker.Worker(self.job)
        work.signals.log.connect(self.log_menu.append)
        self.pool.start(work)
    ######################################################

    def _set_up_buttons(self):
        self.event_button = QPushButton()
        self.webhook_button = QPushButton()
        self.event_button.setText("Force Send Events")
        self.webhook_button.setText("Manage Webhooks")

        self.event_button.setFixedHeight(50)
        self.webhook_button.setFixedHeight(50)

        self.vbox1.addWidget(self.event_button)
        self.vbox1.addWidget(self.webhook_button)

        self.event_button.clicked.connect(lambda: self.switch_buttons("events"))
        self.webhook_button.clicked.connect(lambda: self.switch_buttons("webhook"))
    
    def _init_event_widgets(self):
        self.log_menu = QTextEdit()
        self.log_menu.setReadOnly(True)
        self.log_menu.setMinimumWidth(100)
        self.log_menu.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.vbox2.addWidget(self.log_menu)
        self.log_menu.hide()
    def _init_webhook_widgets(self):
        self.webhook = webhook_subwindow.SubWindow(self.vbox2)
        self.webhook.button.hide()


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