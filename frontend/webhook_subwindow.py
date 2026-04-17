import sys
from PySide6.QtCore import Qt, QThreadPool
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                                QHBoxLayout, QPushButton, QTextEdit,
                                QSizePolicy, QLineEdit, QLabel, QScrollArea, QSpacerItem)
from . import settings, worker
from backend import json_handler

class SubWindow(QWidget):
    def __init__(self, save_json, log_signal):
        super().__init__()
        self.setup(save_json, log_signal)
        self.scroll_area()
        self.webhook_layout()
    
    def setup(self, save_json, log_signal):
        self.save_json = save_json
        self.log_signal = log_signal
        self.json_handler = json_handler
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
        
        self.content_layout.setSpacing(6)
        
        scroll.setWidget(content)
        self.main_layout.addWidget(scroll)
        
    def webhook_layout(self):
        for game in self.games:
            container = QWidget()
            container.setObjectName("StyleWebhook")
            container.setAttribute(Qt.WA_StyledBackground, True)
            
            label = QLabel(game)
            webhook_line = QLineEdit("Insert Webhook")
            save_button = QPushButton("Save")
            
            vbox = QVBoxLayout(container)
            vbox.setContentsMargins(10,10,10,10)
            vbox.setSpacing(2)
            hbox = QHBoxLayout()
            hbox.setContentsMargins(0, 0, 0, 0)

            vbox.addWidget(label)
            hbox.addWidget(webhook_line, 3)
            hbox.addWidget(save_button, 1)
            
            save_button.clicked.connect(lambda checked, webhook=webhook_line, label=label: self.on_click(webhook,label))
            
            self.games_dict[game] = {
                "label": label,
                "webhook_line": webhook_line,
                "save_button": save_button,
            }
            label.hide()
            webhook_line.hide()
            save_button.hide()
            vbox.addLayout(hbox)
            self.content_layout.addWidget(container)
    
    def on_click(self, webhook_line, label):
        text = webhook_line.text()
        if not text.startswith("https"):
            # perchance invalid popup
            self.log_signal("Invalid link.")
            print("Invalid link.")
        else:
            game_name = label.text()
            print(game_name, text)
            self.save_json(game_name, "webhook", text)
        