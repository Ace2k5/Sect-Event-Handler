import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
import settings

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self._init_window_settings()
        
    def _init_window_settings(self):
        layout = QHBoxLayout(self)
        
        window_title = settings.window_settings['window_name']
        w, h = settings.window_settings['resolution']
        
        self.setWindowTitle(window_title)
        self.resize(w, h)
        
        self._set_stylesheet()
        self._set_up_buttons(layout)
    
    def _set_up_buttons(self, box):
        button = QPushButton()
        button.setText("TEST")
        
        
        
        box.addWidget(button, alignment=Qt.AlignVCenter)
    
    def _set_stylesheet(self):
        self.setStyleSheet('''
                        QWidget {
                            background-color: #1b1b1f;
                        }
                            
                        QPushButton {
                            color: white;    
                        }
                        ''')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()