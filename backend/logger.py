"""
Custom logging module for Sect-Event-Handler.

Provides a unified logging interface with console and file output,
plus optional GUI signal emission for real-time log display.
"""

import logging
from pathlib import Path

print("[DEBUG] logger.py module is being loaded")

class Log():
    """
    Custom logging class that provides both console and file logging capabilities.
    
    This class wraps Python's standard logging module to provide:
    - Console output (stdout)
    - File logging to backend/info.log
    - Optional GUI signal emission for PySide6 applications
    - Consistent log format across all outputs
    
    Log format: "DATE: {timestamp} | LEVEL: {level} | MSG: {message}"
    """
    def __init__(self, signals=None):
        """
        Initializes the Log instance with console and file handlers.
        
        Args:
            signals: Optional signals object for GUI communication.
                    If provided, log messages will also be emitted as signals
                    for real-time display in PySide6 applications.
                    
        Notes:
            - Creates two handlers: console (stdout) and file (backend/info.log)
            - Sets log level to INFO by default
            - Uses append mode for log file to preserve history
            - UTF-8 encoding for international character support
        """
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
        """
        Logs an informational message.
        
        Args:
            str: The informational message string to log
            
        Notes:
            - Logs at INFO level
            - Appears in both console and log file
            - Emits signal for GUI display if signals object provided
        """
        self.logger.info(str)
        if self.signals:
            self.signals.emit(f"INFO: {str}")
        
    def log_warning(self, str: str):
        """
        Logs a warning message.
        
        Args:
            str: The warning message string to log
            
        Notes:
            - Logs at WARNING level
            - Appears in both console and log file
            - Emits signal for GUI display if signals object provided
        """
        self.logger.warning(str)
        if self.signals:
            self.signals.emit(f"WARNING: {str}")
        
    def log_error(self, str: str):
        """
        Logs an error message with exception information.
        
        Args:
            str: The error message string to log
            
        Notes:
            - Logs at ERROR level with exc_info=True (includes traceback)
            - Appears in both console and log file
            - Emits signal for GUI display if signals object provided
            - Includes exception traceback in log file for debugging
        """
        self.logger.error(str, exc_info=True)
        if self.signals:
            self.signals.emit(f"ERORR: {str}")
        
    def check_handlers(self):
        """
        Checks and returns the current logging handlers.
        
        Returns:
            list: List of logging handlers attached to the logger
            
        Notes:
            - Useful for debugging logging configuration
            - Typically returns [StreamHandler, FileHandler]
        """
        self.logging.handlers