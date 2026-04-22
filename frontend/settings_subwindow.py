import sys
from PySide6.QtCore import Qt, QThreadPool, Signal
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                                QHBoxLayout, QPushButton, QTextEdit,
                                QSizePolicy, QLineEdit, QLabel, QScrollArea, QSpacerItem)
from . import settings, worker
from backend import json_handler

class SubWindow(QWidget):
    settings_signal = Signal(str)
    def __init__(self, save_settings, log_signal):
        super().__init__()
        self.setup(save_settings, log_signal)
        
    def setup(self, save_settings, log_signal):
        self.save_settings = save_settings
        self.log_signal = log_signal
        
        self.button = QPushButton("Click")
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        
        self.lookback = QLineEdit("Add days to look back")
        self.save = QPushButton("Save")
        self.save.clicked.connect(lambda: self.on_click_lookback())
        self.hbox.addWidget(self.lookback, 3)
        self.hbox.addWidget(self.save, 1)
        
        
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.button)
        self.vbox.addSpacerItem(QSpacerItem(50, 1000, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addLayout(self.vbox)
        
    def on_click_lookback(self):
        try:
            text = int(self.lookback.text())
            self.save_settings("lookback_days", text)
            self.log_signal("FRONTEND: Successfully changed days to look back.")
            print("FRONTEND: Successfully changed days to look back.")
        except ValueError as e:
            self.log_signal("FRONTEND: Invalid value. Please use integers only.")
            print("FRONTEND: Invalid value. Please use integers only.")