import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from .. import inits

class BaseScraper(ABC):
    def __init__(self):
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
    def format_events(self, row_data):
        '''Abstract method for formatting events - implemented by subclasses'''
        pass
    
    @abstractmethod
    def data_getter(self):
        '''Abstract method for main data retrieval flow - implemented by subclasses'''
        pass