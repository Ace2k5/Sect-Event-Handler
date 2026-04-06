import requests
from .base_scraper import BaseScraper
from bs4 import BeautifulSoup
from datetime import date
from .. import backend_inits, utils
from urllib.parse import urljoin

class LimbusScraper(BaseScraper):
    def __init__(self, logger, user_data=None):
        super().__init__(logger=logger, user_data=user_data)
        self.logger = logger
        self.game = self.user_data["Limbus Company"]
 
    def find_events(self, soup, url, table_class) -> list:
        '''
        Searches for Limbus Company events in the HTML table for a specific month/year.
        
        Args:
            soup: BeautifulSoup parser object for the URL HTML content
            table_class: CSS class name of the HTML table to search for
            game: Name of the game (e.g., "Limbus Company")
            dates_format: String in format "Month Year" (e.g., "November 2025")
            
        Returns:
            List of lists containing event data: [[event_name, start_date, end_date], ...]
            Returns None if soup is None
        ''' 
        if soup is None:
            self.logger.log_info("Soup is none in Limbus Company")
            raise
        found_events = []
        self.logger.log_info(f"Currently in {self.game['proper_name']}")
        events = soup.find_all("table", class_=table_class)
        for table in events: # iterates everything inside the table_class
            rows = table.find_all("tr")
            for row in rows: # delves deeper into tr
                cells = row.find_all("td") # gets string from td
                if cells:
                    img = ""
                    row_data = []
                    for cell in cells: # ['', 'event', 'event_start', 'event_end']
                        img = cell.find("img")
                        if img:
                            src = img.get("src", "")
                            img_url = urljoin(url, src)
                        text = cell.get_text(strip=True) # remove unnecessary text
                        if text == "":
                            continue
                        else:
                            row_data.append(text)
                    row_data.append(img_url)
                    found_events.append(row_data)
        found_events = utils.deduplication(found_events, self.logger)
        return found_events

    def format_events(self, found_events):
        lookback = self.user_data['lookback_days']
        format_events = []
        event_date = ""
        for data in found_events:
            if len(data) > 2:
                event_name = data[0]
                event_date = f"{data[1]} - {data[2]}"
                event_img_url = data[3]
                if utils.is_relevant_date(event_date, lookback):
                    format_events.append({
                        "name": event_name,
                        "image": event_img_url,
                        "fields": [
                            {"name": "Date", "value":event_date, "inline":True}
                        ]
                    })
            else:
                self.logger.log_info(f"{data} did not meet the requirements, skipping...")
                continue
        
        return format_events

    def data_getter(self, forced=False):
        try:
            if self.game["webhook"].startswith("https"):
                site_config = self.sites[1]
                table, url = site_config
                soup = self.get_response(url)
                if soup is None:
                    raise ValueError("Could not get HTML data in BaseScraper get_response function.")
                data = self.find_events(soup, url, table)
                formatted = self.format_events(data)
                formatted_formatted = self.update_local_events(formatted, forced)
                return formatted_formatted
            else:
                self.logger.log_error("Limbus Company does not have a valid URL in the local files.")
                return None
        except Exception as e:
            self.logger.log_error(f"Error occured as {e} in Limbus Company")
        finally:
            self.session.close()