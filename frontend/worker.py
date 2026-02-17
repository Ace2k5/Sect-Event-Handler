from PySide6.QtCore import QThreadPool, QRunnable, Slot, Signal, QObject

class WorkerSignals(QObject):
    finished = Signal()
    log = Signal(str)
    error = Signal(str)

class Worker(QRunnable):
    def __init__(self, job):
        super().__init__()
        self.job = job
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            self.job(self.signals)
        except Exception as e:
            self.signals.error.emit(str(e))
        finally:
            self.signals.finished.emit()

