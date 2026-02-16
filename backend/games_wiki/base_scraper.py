import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from .. import inits, json_handler
from pathlib import  Path
import json

class BaseScraper(ABC):
    def __init__(self, logger, window=None):
        self.window = window
        self.user_data = json_handler.get_user_data()
        self.sites = inits.SITES
        self.session = requests.Session()
        self.logger = logger
    
    def get_response(self, url):
        '''
        Fetches the HTML content from a URL and parses it with BeautifulSoup.
        
        Args:
            url: Website URL to scrape
            
        Returns:
            BeautifulSoup object if request is successful (status 200), None otherwise
        '''
        try:
            response = self.session.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                return soup
            else:
                self.logger.info(f"Response status: {response.status_code}")
                if self.window:
                    self.window.log_menu.append(f"Response status: {response.status_code}")
                return None
        except requests.RequestException as e:
            if self.window:
                self.window.log_menu.append(f"get_response returned as {e}")
            raise requests.RequestException(f"get_response returned as {e}")
    
    @abstractmethod
    def find_events(self, soup, table_class, game, dates_format):
        '''
        Abstract method for finding events in HTML tables.
        Implemented by subclasses for game-specific scraping.
        
        Args:
            soup: BeautifulSoup parser object
            table_class: CSS class name of HTML tables
            game: Name of the game
            dates_format: Date format string for filtering events
        
        Returns:
            List of event data rows
        '''
        pass
    
    @abstractmethod
    def find_img(self, soup: BeautifulSoup, url: str, table_class: str, game: str) -> list[dict]:
        '''
        Abstract method for downloading and linking event images.
        Implemented by subclasses for game-specific image handling.
        
        Args:
            soup: BeautifulSoup parser object
            url: Base URL of the game wiki
            table_class: CSS class name of images to find
            game: Name of the game
        
        Returns:
            List of dictionaries with Image_Name and Image_URL
        '''
        pass
    
    @abstractmethod
    def link_imgs(self, dictionary_of_events: list[dict], list_of_imgs: list[dict]) -> list[dict]:
        '''
        Abstract method for linking images to events.
        Implemented by subclasses.
        
        Args:
            dictionary_of_events: List of event dictionaries
            list_of_imgs: List of image dictionaries
        
        Returns:
            List of events with image URLs linked
        '''
        pass
    
    @abstractmethod
    def format_events(self, row_data):
        '''
        Abstract method for formatting raw event data.
        Implemented by subclasses for game-specific formatting.
        
        Args:
            row_data: List of raw event rows from find_events
        
        Returns:
            List of formatted event dictionaries
        '''
        pass
    
    @abstractmethod
    def data_getter(self):
        '''
        Abstract method for the main data retrieval flow.
        Orchestrates fetching, finding, and formatting events.
        Implemented by subclasses.
        
        Returns:
            List of formatted events ready for output
        '''
        pass