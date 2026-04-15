from PySide6.QtCore import QRunnable, QThreadPool

class RunOnStartup(QRunnable):
    def __init__(self, start):
        super().__init__()
        self.start = start

    def run(self):
        self.start()
