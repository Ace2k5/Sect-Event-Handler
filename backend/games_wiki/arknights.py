import requests
import json
from .base_scraper import BaseScraper
from bs4 import BeautifulSoup
from datetime import date
from .. import inits, utils
from pathlib import Path
from urllib.parse import urljoin

class ArkScraper(BaseScraper):
    '''
    THESE IMPLEMENTATIONS ARE STRICTLY FOR AK ONLY!!!!!!!!
    '''
    def __init__(self, logger):
        super().__init__(logger=logger)
        '''base class contains:
        self.user_data = {game {webhook, proper game name}}
        self.sites {table class, link to game wiki}
        self.sessions
        self.logger
        '''
        self.path_imgs = Path(__file__).parent.parent.parent / "arknights_imgs"
        self.game = self.user_data['arknights']
        
    def find_events(self, soup, table_text, url):
        '''
        searches tables for the events

        (LOOP BASICALLY GOES LIKE:
        Tables/ (MAIN TABLE CLASS)
            Table1/ (THE TABLE INSIDE THE MAIN TABLE CLASS)
                Row1/ (THE ROW)
                Cell1 (CONTENTS OF THAT ROW)
                Cell2)
        
        Args:
            soup: BeautifulSoup parser object for the URL HTML content
            table_text: CSS class name of the HTML table to search for
            game_name: Name of the game (e.g., "Arknights")
            
        Returns:
            List of lists containing event data: [event_name, date_string, ...]
        '''
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

    def find_img(self, soup: BeautifulSoup, url: str, tables: str) -> list[dict]:
        pass

    def format_events(self, row_data: list[list[str]]) -> list[dict]:
        '''
        removes CN and Global in the strings of row_data, only grabs dates(row[1]) and event name(row[0])
        
        Args:
            row_data: List of raw event rows from find_events: [[event_name, date_string], ...]
                      where date_string contains "CN:" and "Global:" markers
            
        Returns:
            list of dictionary:
            [
                {
                    "Event": str (event name),
                    "CN": str normalized CN date range (ex. Sep 04, 2025 – Sep 18, 2025)
                    "Global": str normalized Global date range (ex. Feb 10, 2026 – Feb 24, 2026)
                },
                ...
            ]
            Returns None if date parsing fails
        '''
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
                "Event": event_name,
                "CN": normalized_cn,
                "Global": normalized_global,
                "Event_PNG": event_png
            })
        return clean_format
    
    def link_imgs(self, dictionary_of_events: list[dict], list_of_imgs: list[dict]) -> list[dict]:
        pass
            
    def data_getter(self):
        '''    
        Returns:
            List of dictionaries with complete event information:
            [
                {
                    "Matched_Event_IMGS": dict (matched event metadata),
                    "CN": str (CN release date range (DATE ONLY)),
                    "Global": str (Global release date range (DATE ONLY)),
                    "Event_PNG": str (URL to event banner image)
                },
                ...
            ]
        '''
        try:
            if self.user_data['arknights']['webhook']:
                site_config = self.sites[0]
                table, url = site_config
                soup = self.get_response(url)
                if soup is None:
                    raise ValueError("Could not get HTML data in BaseScraper get_response function.")
                
                events = self.find_events(soup, table, url)
                formatted_data = self.format_events(events)
                return formatted_data
            else:
                self.logger.log_info("Arknights has no active webhook, skipping...")
        except Exception:
            raise
        finally:
            self.session.close()