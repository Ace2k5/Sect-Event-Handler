import sys
from PySide6.QtCore import Qt, QThreadPool, Signal
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                                QHBoxLayout, QPushButton, QTextEdit,
                                QSizePolicy, QLineEdit, QLabel, QScrollArea)
from . import settings, worker
from backend import json_handler

class SubWindow(QWidget):
    settings_signal = Signal(str)
    def __init__(self):
        super().__init__()
        self.setup()
        
    def setup(self):
        self.button = QPushButton("Click")
        self.vbox = QVBoxLayout()
        
        self.vbox.addWidget(self.button)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addLayout(self.vbox)