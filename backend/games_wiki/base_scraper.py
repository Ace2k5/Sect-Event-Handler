import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from .. import inits, json_handler
from pathlib import  Path
import json

class BaseScraper(ABC):
    def __init__(self):
        self.user_data = json_handler.get_user_data()
        self.sites = inits.SITES
        self.session = requests.Session()
    
    def get_response(self, url):
        '''
        Args:
            url: Website URL to scrape
            
        Returns:
            BeautifulSoup object or None if request fails
        '''
        try:
            response = self.session.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                return soup
            else:
                print(f"Response status: {response.status_code}")
                return None
        except requests.RequestException as e:
            raise requests.RequestException(f"get_response returned as {e}")
    
    @abstractmethod
    def find_events(self, soup, table_class, game, dates_format):
        '''Abstract method for finding events - implemented by subclasses'''
        pass
    
    @abstractmethod
    def find_img(self, soup: BeautifulSoup, url: str, table_class: str, game: str) -> list[dict]:
        pass
    
    @abstractmethod
    def link_imgs(self, dictionary_of_events: list[dict], list_of_imgs: list[dict]) -> list[dict]:
        pass
    
    @abstractmethod
    def format_events(self, row_data):
        '''Abstract method for formatting events - implemented by subclasses'''
        pass
    
    @abstractmethod
    def data_getter(self):
        '''Abstract method for main data retrieval flow - implemented by subclasses'''
        pass