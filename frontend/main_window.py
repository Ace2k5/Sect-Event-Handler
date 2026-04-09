import sys
from PySide6.QtCore import Qt, QThreadPool, QTimer
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                                QHBoxLayout, QPushButton, QTextEdit,
                                QSizePolicy, QSpacerItem)
from . import settings, worker, webhook_subwindow
from backend import flow

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()
        
    def setup(self):
        self.runner = None
        self.work_signals = None
        self.web_subwindow = None
        self.pool = QThreadPool()
        self.sizes = settings.pyside_size
        self.window_settings()
        self._init_event_widgets()
        self.worker_thread(forced=False)
        self._set_stylesheet()

    def switch_buttons(self, mode):
        if mode == "events":
            self.webhook.hide()
            for game in self.webhook.games_dict:
                self.webhook.games_dict[game]['label'].hide()
                self.webhook.games_dict[game]['webhook_line'].hide()
                self.webhook.games_dict[game]['save_button'].hide()
            self.log_menu.show()
        elif mode == "webhook":
            if self.web_subwindow is None:
                self._init_webhook_widgets(self.runner)
            self.log_menu.hide()
            self.webhook.show()
            for game in self.webhook.games_dict:
                self.webhook.games_dict[game]['label'].show()
                self.webhook.games_dict[game]['webhook_line'].show()
                self.webhook.games_dict[game]['save_button'].show()
        
    def window_settings(self):
        self.buttons_size = self.sizes['button_size']
        self.log_size = self.sizes['log_menu_size']
        layout = QHBoxLayout(self)
        self.vbox1 = QVBoxLayout()
        self.vbox2 = QVBoxLayout()


        window_title = settings.window_settings['window_name']
        w, h = settings.window_settings['resolution']
        
        self.setWindowTitle(window_title)
        self.resize(w, h)
    
        self._set_up_buttons()

        layout.addLayout(self.vbox1, 2)
        layout.addLayout(self.vbox2, 3)

    # Worker thread for backend.
    def job(self, signals, forced=True):
        if self.runner is None:   
            self.runner = flow.ScrapeFlow(signals)
        self.runner.flow(forced=forced)

    def worker_thread(self, forced=True):
        work = worker.Worker(self.job, forced=forced)
        if not self.work_signals:
            self.work_signals = work.signals.log.connect(self.log_menu.append)
        self.pool.start(work)
    ######################################################

    def _set_up_buttons(self):
        self.event_button = QPushButton()
        self.webhook_button = QPushButton()
        self.event_button.setText("Force Send Events")
        self.webhook_button.setText("Manage Webhooks")

        self.event_button.setFixedHeight(self.buttons_size)
        self.webhook_button.setFixedHeight(self.buttons_size)

        self.vbox1.addWidget(self.event_button)
        self.vbox1.addWidget(self.webhook_button)
        self.vbox1.addSpacerItem(QSpacerItem(50, 50, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.event_button.clicked.connect(lambda: self.switch_buttons("events"))
        self.webhook_button.clicked.connect(lambda: self.switch_buttons("webhook"))
        self.event_button.clicked.connect(lambda: QTimer.singleShot(300, self.worker_thread()))
    
    def _init_event_widgets(self):
        self.log_menu = QTextEdit()
        self.log_menu.setReadOnly(True)
        self.log_menu.setMinimumWidth(self.log_size)
        self.log_menu.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.vbox2.addWidget(self.log_menu)
    def _init_webhook_widgets(self, runner):
        self.webhook = webhook_subwindow.SubWindow(runner=runner)
        self.vbox2.addWidget(self.webhook)
        self.webhook.hide()


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
                           
                        #ScrollArea {
                            background-color: #121210;
                        }
                        #SubWindow {
                            background-color: #121210;
                        }
                        #SubWindow QScrollArea {
                            border: none;
                        }
                        
                        #StyleWebhook {
                            background-color: #121210;
                        }
                        ''')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()