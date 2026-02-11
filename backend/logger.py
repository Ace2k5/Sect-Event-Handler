import logging
from pathlib import Path

class Log():
    def __init__(self):
        logging.basicConfig(
            filename=Path(__file__).parent / "./info.log",
            format= "%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d | %H:%M:%S"
        )
        
        
        
        
a = Log()