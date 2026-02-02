import requests
from .base_scraper import BaseScraper
from bs4 import BeautifulSoup
from datetime import date
from .. import inits, get_time, utils

class ArkScraper(BaseScraper):
    def __init__(self):
        self.sites = inits.SITES # (TABLE CLASS, URL, GAME)
        self.dates = get_time.getTime()

    # Arknights ###################################################################################################################
    def find_events(self, soup, table_text, game_name, date_formats):
        '''
        Args:
            soup: parser for the URL
            table_text: HTML class
            game_name: Name of the game
            date_formats: a list containing multiple formats of yyyy-mm-dd
            
        returns:
            A list containing all of the events of Arknights
        '''

        LOOKBACK_DAYS = 30

        if game_name == "Arknights":
            if soup is None:
                print("No HTML content to parse!")
                return
            
            
            events = soup.find_all("table", class_=table_text)
            print(f"Currently in {game_name}")
            found_events = []
            for table in events:
                rows = table.find_all('tr') # find all headers
                for row in rows:
                    cells = row.find_all('td') # find all data cells
                    if cells:
                        row_data = []
                        for cell in cells:
                            text = cell.get_text(strip=True)
                            row_data.append(text)
                            if len(row_data) > 1:
                                date_text = row_data[1]
                                if utils.is_relevant_date(date_text, lookback_days=LOOKBACK_DAYS):
                                    found_events.append(row_data)
            
            return found_events
        else:
            print("Arknights does not exist. Please fix.")
            return
                        
    
    def format_events(self, row_data):
        '''
        Args:
            row_data: A list containing each events found in Arknights by a pair of strings
            
        returns:
            A list that contains a list [Event Name, Date]
        '''
        
        set_events = utils.deduplication(row_data)
        if set_events is None:
            print("Events is None, deduplication problem")
            return
            
        list_events = list(set_events)

        clean_format = []

        for row in list_events:
            event_name = row[0]
            date_str = row[1]

            cn_date = None
            if "CN:" in date_str:
                cn_date_part = date_str.split("CN:")[1]
                cn_date_temp = cn_date_part.split("Global:")[0].strip() if "Global:" in cn_date_part else cn_date_part.strip()
                cn_date = cn_date_temp.split("(")[0].strip()
                normalized_cn = utils.normalize_date_range(cn_date)

            global_date = None
            if "Global:" in date_str:
                global_date_part = date_str.split("Global:")[1]
                global_date = global_date_part.split("(")[0].strip()
                normalized_global = utils.normalize_date_range(global_date)

            clean_format.append({
                "Event": event_name,
                "CN": normalized_cn,
                "Global": normalized_global
            })
        return clean_format
            
    def data_getter(self):
        site_config = self.sites[0]
        table, url, game = site_config
        response = self.get_response(url)
        events = self.find_events(response, table, game, self.dates)
        data = self.format_events(events)
        return data
    