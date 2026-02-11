import logging
from pathlib import Path

print("[DEBUG] logger.py module is being loaded")

class Log():
    def __init__(self):
        print(f"[DEBUG] Log.__init__ called - Creating new logger instance")
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Check if handlers already exist to avoid duplicates
        existing_handlers = [h for h in self.logger.handlers if isinstance(h, logging.StreamHandler)]
        print(f"[DEBUG] Existing stream handlers: {len(existing_handlers)}")
        
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
        self.logger.info(str)
        
    def log_warning(self, str: str):
        self.logger.warning(str)
        
    def log_error(self, str: str):
        self.logger.error(str)
        
    def check_handlers(self):
        self.logging.handlers