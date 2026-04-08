from PySide6.QtCore import QThreadPool, QRunnable, Slot, Signal, QObject

class WorkerSignals(QObject):
    finished = Signal()
    log = Signal(str)
    error = Signal(str)

class Worker(QRunnable):
    def __init__(self, job, forced=False):
        super().__init__()
        self.job = job
        self.signals = WorkerSignals()
        self.forced = forced

    @Slot()
    def run(self):
        try:
            self.job(self.signals, self.forced)
        except Exception as e:
            self.signals.error.emit(str(e))
        finally:
            self.signals.finished.emit()