import sys
from PySide6.QtCore import Qt, QThreadPool
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                                QHBoxLayout, QPushButton, QTextEdit,
                                QSizePolicy, QLineEdit, QLabel, QScrollArea)
from . import settings, worker

class SubWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()
        self.scroll_area()
        self.webhook_layout()
    
    def setup(self):
        self.setObjectName("SubWindow")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.games = settings.games_supported
        self.games_dict = {}
        self.main_layout = QVBoxLayout(self)
        
    def scroll_area(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        content = QWidget()
        content.setObjectName("ScrollArea")
        content.setAttribute(Qt.WA_StyledBackground, True)
        self.content_layout = QVBoxLayout(content)
        
        scroll.setWidget(content)
        self.main_layout.addWidget(scroll)
        
    def webhook_layout(self):
        for game in self.games:
            container = QWidget()
            container.setObjectName("StyleWebhook")
            container.setAttribute(Qt.WA_StyledBackground, True)
            
            label = QLabel(game)
            webhook_button = QLineEdit("Insert Webhook")
            save_button = QPushButton("Save")
            
            vbox = QVBoxLayout(container)
            hbox = QHBoxLayout()

            vbox.addWidget(label)
            hbox.addWidget(webhook_button)
            hbox.addWidget(save_button)
            
            save_button.clicked.connect(lambda checked, webhook=webhook_button, save=save_button: self.on_click(webhook, save))
            
            self.games_dict[game] = {
                "label": label,
                "webhook_button": webhook_button,
                "save_button": save_button,
            }
            label.hide()
            webhook_button.hide()
            save_button.hide()
            vbox.addLayout(hbox)
            self.content_layout.addWidget(container)
    
    def on_click(self, webhook_button, save_button):
        text = str(webhook_button.text())
        print(text)