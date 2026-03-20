"""
Base scraper class providing common functionality for game wiki scrapers.

This abstract base class defines the interface and common implementation
for game-specific scrapers. Subclasses must implement the abstract methods
for game-specific HTML parsing and data formatting.
"""

import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from .. import inits, json_handler
from pathlib import Path
import json

class BaseScraper(ABC):
    """
    Abstract base class for game wiki scrapers.
    
    Provides common functionality for:
    - HTTP session management
    - HTML fetching and parsing
    - User configuration access
    - Logging
    
    Subclasses must implement:
    - find_events(): Game-specific HTML table parsing
    - format_events(): Game-specific data formatting
    - data_getter(): Main data retrieval workflow
    """
    def __init__(self, logger):
        """
        Initializes the base scraper with common dependencies.
        
        Args:
            logger: Logger object for logging messages
            
        Attributes:
            user_data: Dictionary of user configuration from JSON file
            sites: List of (table_class, url) tuples for scraping
            session: requests.Session for HTTP requests
            logger: Logger instance for logging
        """
        self.user_data = json_handler.get_user_data()
        self.sites = inits.SITES
        self.session = requests.Session()
        self.logger = logger


        
    def get_response(self, url):
        """
        Fetches HTML content from a URL and parses it with BeautifulSoup.
        
        Args:
            url: Website URL to scrape
            
        Returns:
            BeautifulSoup: Parsed HTML document if request succeeds (status 200)
            
        Raises:
            requests.ConnectionError: If HTTP request fails or returns non-200 status
            requests.RequestException: For other request-related errors
            
        Notes:
            - Uses shared session for connection pooling
            - Returns BeautifulSoup object with 'html.parser'
            - Logs non-200 status codes before raising exception
        """
        try:
            response = self.session.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                return soup
            else:
                self.logger.info(f"Response status: {response.status_code}")
                raise requests.ConnectionError
        except requests.RequestException as e:
            raise requests.RequestException(f"get_response returned as {e}")
    
    @abstractmethod
    def find_events(self, soup, table_class, game, dates_format):
        """
        Abstract method for finding events in HTML tables.
        
        Must be implemented by subclasses for game-specific HTML parsing.
        
        Args:
            soup: BeautifulSoup parser object containing HTML document
            table_class: CSS class name of HTML tables containing events
            game: Name of the game (for logging and context)
            dates_format: Date format string for filtering events
            
        Returns:
            list: List of raw event data rows, typically [[event_name, date_string, ...], ...]
            
        Notes:
            - Implementation should search for tables with specified CSS class
            - Should extract event names, dates, and any relevant metadata
            - Should handle game-specific HTML structure variations
        """
        pass

    @abstractmethod
    def format_events(self, row_data):
        """
        Abstract method for formatting raw event data.
        
        Must be implemented by subclasses for game-specific data formatting.
        
        Args:
            row_data: List of raw event rows from find_events()
            
        Returns:
            list: List of formatted event dictionaries ready for Discord webhook
            
        Notes:
            - Implementation should parse and normalize dates
            - Should filter events based on relevance (lookback days)
            - Should structure data for Discord embed format
            - May include game-specific fields and metadata
        """
        pass

    @abstractmethod
    def data_getter(self):
        """
        Abstract method for the main data retrieval flow.
        
        Must be implemented by subclasses to orchestrate the complete
        scraping and formatting workflow for a specific game.
        
        Returns:
            list: List of formatted event dictionaries for new events only,
                  or None if no events found or webhook not configured.
                  
        Notes:
            - Implementation should coordinate: get_response(), find_events(), format_events()
            - Should handle error cases gracefully
            - Should check webhook configuration before scraping
            - Should return only new events (not previously seen)
        """
        pass