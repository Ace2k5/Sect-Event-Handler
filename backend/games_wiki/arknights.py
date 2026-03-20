import requests
import json
from .base_scraper import BaseScraper
from bs4 import BeautifulSoup
from datetime import date
from .. import inits, utils, json_handler
from pathlib import Path
from urllib.parse import urljoin

class ArkScraper(BaseScraper):
    """
    Arknights-specific web scraper for extracting event data from the Arknights wiki.
    
    This class implements game-specific logic for:
    - Finding event tables in Arknights wiki HTML structure
    - Parsing CN and Global date formats unique to Arknights
    - Formatting event data for Discord embeds
    - Tracking seen events to avoid duplicate notifications
    
    Inherits from BaseScraper which provides common scraping functionality.
    """
    def __init__(self, logger):
        """
        Initializes the ArkScraper with Arknights-specific configuration.
        
        Args:
            logger: Logger object for logging messages
            
        Notes:
            - Inherits from BaseScraper which provides:
              * self.user_data: User configuration dictionary
              * self.sites: List of (table_class, url) tuples for scraping
              * self.session: requests.Session for HTTP requests
              * self.logger: Logger instance
            - Sets up path for Arknights image storage
            - References Arknights-specific configuration from user_data
        """
        super().__init__(logger=logger)
        self.path_imgs = Path(__file__).parent.parent.parent / "arknights_imgs"
        self.game = self.user_data['Arknights']
        
    def find_events(self, soup, table_text, url):
        """
        Extracts event data from HTML tables in the Arknights wiki.
        
        Searches for tables with the specified CSS class, then iterates through
        rows and cells to extract event names, dates, and image URLs.
        
        Args:
            soup: BeautifulSoup parser object for the URL HTML content
            table_text: CSS class name of the HTML table to search for
            url: Base URL of the page (for resolving relative image URLs)
            
        Returns:
            List of lists containing event data: 
            [[event_name, date_string, image_url], ...]
            
        Notes:
            - Processes tables with class matching table_text
            - Extracts text from all <td> cells in each row
            - Finds and resolves image URLs to absolute paths
            - Returns None if connection error occurs
        """
        events = soup.find_all("table", class_=table_text)

        self.logger.log_info(f"Currently in {self.game['proper_name']}")
        found_events = []
        try:
            for table in events:
                rows = table.find_all('tr') # find all headers
                for row in rows:
                    cells = row.find_all('td') # find all data cells
                    if cells:
                        row_data = []
                        img = ""
                        for cell in cells:
                            img = cell.find("img")
                            if img:
                                src = img.get("src", "")
                                img_url = urljoin(url, src)
                            text = cell.get_text(strip=True)
                            self.logger.log_info(f"Appending {text} to row_data...")
                            row_data.append(text)
                        row_data.append(img_url)
                        found_events.append(row_data)
            print(found_events)
            return found_events
        except requests.ConnectionError as e:
            self.logger.log_error(f"Connection error: {e}")
            return None
        except Exception as e:
            self.logger.log_error(f"Unknown error occured: {e}")

    def format_events(self, row_data: list[list[str]]) -> list[dict]:
        """
        Formats raw event data into structured dictionaries for Discord embeds.
        
        Processes Arknights-specific date format containing both CN and Global dates,
        normalizes them, filters by relevance, and structures for Discord webhook.
        
        Args:
            row_data: List of raw event rows from find_events: 
                     [[event_name, date_string, image_url], ...]
                     where date_string contains "CN:" and "Global:" markers
            
        Returns:
            list: List of dictionaries formatted for Discord webhook:
            [
                {
                    "name": event_name,
                    "image": image_url,
                    "fields": [
                        {"name": "CN Date", "value": normalized_cn_date, "inline": True},
                        {"name": "Global Date", "value": normalized_global_date, "inline": True}
                    ]
                },
                ...
            ]
            
        Raises:
            ValueError: If CN: or Global: markers are missing from date string
            
        Notes:
            - Filters events based on lookback_days configuration
            - Normalizes dates to "Mon DD, YYYY" format
            - Skips events where Global date is not within lookback period
        """
        lookbackdays = self.user_data.get('lookback_days', 30)
        set_events = utils.deduplication(row_data, self.logger)
        if set_events is None:
            raise ValueError("Expected a set, None was returned.")
            
        list_events = list(set_events)

        clean_format = []

        for row in list_events:
            event_name = row[0]
            date_str = row[1]
            event_png = row[2]

            if "CN:" in date_str:
                cn_date_part = date_str.split("CN:")[1]
                cn_date_temp = cn_date_part.split("Global:")[0].strip() if "Global:" in cn_date_part else cn_date_part.strip()
                cn_date = cn_date_temp.split("(")[0].strip()
                normalized_cn = utils.normalize_date_range(cn_date)
            else:
                raise ValueError(f"Could not normalize CN date in {date_str}, format_events function")

            if "Global:" in date_str:
                global_date_part = date_str.split("Global:")[1]
                global_date = global_date_part.split("(")[0].strip()
                if not utils.is_relevant_date(global_date, lookbackdays):
                    continue
                normalized_global = utils.normalize_date_range(global_date)
            else:
                raise ValueError(f"Could not normalize Global date in {date_str}, format_events function")

            clean_format.append({
                "name": event_name,
                "image": event_png,
                "fields": [
                    {"name": "CN Date", "value": normalized_cn, "inline":True},
                    {"name": "Global Date", "value": normalized_global, "inline":True}
                ]
            })
        return clean_format
        
    def update_local_events(self, clean_format):
        """
        Tracks seen events to prevent duplicate notifications.
        
        Compares newly found events with previously seen events stored in
        user configuration, returns only new events, and updates the
        seen events list for future runs.
        
        Args:
            clean_format: List of formatted event dictionaries from format_events()
            
        Returns:
            list: List containing only new events (not previously seen)
            
        Notes:
            - Uses set operations to find difference between seen and new events
            - Updates self.game['seen_events'] in memory
            - Persists updated seen events to JSON file
            - Returns empty list if no new events found
        """
        try:
            formatted_data = list()
            saved_events = set(self.game['seen_events'])
            seen_events = set()

            print(clean_format)
            
            self.logger.log_info("Updating local events...")
            for event in clean_format:
                if event['name'] != "":
                    self.logger.log_info(f"Adding {event['name']} for intersection.")
                    seen_events.add(event['name'])
            self.logger.log_info("Currently finding the difference of events.")
            new_events = seen_events - saved_events
            saved_events = new_events | saved_events
            if not saved_events:
                saved_events = seen_events
            all_saved_events = seen_events & saved_events

            if not all_saved_events:
                all_saved_events = seen_events

            self.logger.log_info(f"Found {new_events} as the difference.")

            self.logger.log_info(f"Currently fetching {new_events}'s dict structure.")
            for event in clean_format:
                if event['name'] in new_events:
                    formatted_data.append(event)
                    self.logger.log_info(f"Found {event['name']}'s dict structure.")

            self.game['seen_events'] = list(all_saved_events)
            print(self.user_data)
            json_handler.save_to_json(self.user_data)
            self.logger.log_info("Updated seen events in the local json.")

            return formatted_data
        except Exception as e:
            self.logger.log_error(f"Error occured as {e} when trying to update local events.")
            
            


    def data_getter(self):
        """
        Main public method to retrieve and process Arknights event data.
        
        Orchestrates the complete scraping workflow:
        1. Checks if webhook is configured
        2. Fetches HTML from Arknights wiki
        3. Extracts event data from tables
        4. Formats and filters events
        5. Updates seen events tracking
        6. Returns new events for notification
        
        Returns:
            list: List of formatted event dictionaries for new events only,
                  or None if no webhook configured or no events found.
                  
        Notes:
            - Returns None if webhook is not configured (doesn't start with "https")
            - Returns None if HTML fetch fails
            - Returns empty list if no new events found
            - Closes HTTP session in finally block
        """
        try:
            if self.game['webhook'].startswith("https"):
                site_config = self.sites[0]
                table, url = site_config
                soup = self.get_response(url)
                if soup is None:
                    raise ValueError("Could not get HTML data in BaseScraper get_response function.")
                
                events = self.find_events(soup, table, url)
                formatted_data = self.format_events(events)
                formatted_formatted_data = self.update_local_events(formatted_data)
                return formatted_formatted_data
            else:
                self.logger.log_info("Arknights has no active webhook, skipping...")
                return None
        except Exception:
            raise
        finally:
            self.session.close()