import logging
from pathlib import Path

print("[DEBUG] logger.py module is being loaded")

class Log():
    '''
    Custom logging class that provides both console and file logging capabilities.
    Initializes logging handlers for streaming and file output.
    '''
    def __init__(self, signals=None):
        print("[DEBUG] Log.__init__ called - Creating new logger instance")
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.signals = signals
        
        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(Path(__file__).parent / "info.log", mode='a', encoding='UTF-8')
        
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        
        formatter = logging.Formatter(
            "DATE: {asctime} | LEVEL: {levelname} | MSG: {message}",
            style="{",
            datefmt = "%Y - %m - %d %H:%M"
        )
        
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        print(f"[DEBUG] Logger setup complete - Total handlers: {len(self.logger.handlers)}")
        
    def log_info(self, str: str):
        '''
        Logs an informational message.
        
        Args:
            str: The message string to log
        '''
        self.logger.info(str)
        if self.signals:
            self.signals.log.emit(f"INFO: {str}")
        
    def log_warning(self, str: str):
        '''
        Logs a warning message.
        
        Args:
            str: The warning message string to log
        '''
        self.logger.warning(str)
        if self.signals:
            self.signals.log.emit(f"WARNING: {str}")
        
    def log_error(self, str: str):
        '''
        Logs an error message.
        
        Args:
            str: The error message string to log
        '''
        self.logger.error(str, exc_info=True)
        if self.signals:
            self.signals.log.emit(f"ERORR: {str}")
        
    def check_handlers(self):
        '''
        Checks and returns the current logging handlers.
        
        Returns:
            list: List of logging handlers attached to the logger
        '''
        self.logging.handlers