import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                                QHBoxLayout, QPushButton, QTextEdit,
                                QSizePolicy)
import settings

class Window(QWidget):
    def __init__(self):
        super().__init__()
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

        layout.addLayout(vbox1)
        layout.addLayout(vbox2)
    
    def test(self):
        self.log_menu.append("TEST TEST TEST")

    def _set_up_buttons(self, vbox1, vbox2):
        button = QPushButton()
        button.setText("TEST")
        
        self.log_menu = QTextEdit()
        self.log_menu.setReadOnly(True)
        self.log_menu.setFixedWidth(600)
        self.log_menu.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        vbox1.addWidget(button, alignment=Qt.AlignVCenter)
        vbox2.addWidget(self.log_menu, alignment=Qt.AlignVCenter)
        button.clicked.connect(self.test)

    def _set_stylesheet(self):
        self.setStyleSheet('''
                        QWidget {
                            background-color: #1b1b1f;
                            color: white;
                        }
                            
                        QPushButton {
                            color: white;    
                        }
                           
                        QTextEdit {
                           background-color: #08080F;
                           }
                        ''')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()