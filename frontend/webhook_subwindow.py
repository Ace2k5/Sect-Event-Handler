import sys
from PySide6.QtCore import Qt, QThreadPool
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                                QHBoxLayout, QPushButton, QTextEdit,
                                QSizePolicy)
from . import settings, worker
from backend import flow


class SubWindow(QWidget):
    def __init__(self, vbox2):
        super().__init__()
        self.vbox2 = vbox2
        self.test()

    def test(self):
        self.button = QPushButton("TEST")
        self.vbox2.addWidget(self.button)