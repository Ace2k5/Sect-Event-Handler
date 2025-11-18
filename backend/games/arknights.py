import requests
from bs4 import BeautifulSoup
from datetime import date
from .. import inits, get_time, utils

class ArkScraper():
    def __init__(self):
        self.sites = inits.SITES # (TABLE CLASS, URL, GAME)
        self.dates = get_time.getTime()
        
            
    def get_response(self, url):
        '''
        Args:
            url: Contained inside of a tuple located in inits.py, the 3rd iteration.
        
        '''
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                return soup
        except requests.exceptions.RequestException as e:
            print(f"Problem appeared as {e}")
            return None
                
    # Arknights ###################################################################################################################
    def find_arknights_events(self, soup, table_text, game_name, date_formats):
        '''
        Args:
            soup: parser for the URL
            table_text: HTML class
            game_name: Name of the game
            date_formats: a list containing multiple formats of yyyy-mm-dd
            
        The goal of this function is to find the current events inside of the Arknights Wiki.
        '''
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
                        for date_format in date_formats:
                            if date_format in row_data[1]:
                                found_events.append(row_data)
            return found_events
        else:
            print("Arknights does not exist. Please fix.")
            return
                        
    
    def format_arknights(self, row_data):
        '''
        Args:
            row_data: A list containing each events found in Arknights by a pair of strings
            
        The goal of this function is to format the extracted events info in Arknights.
        '''
        
        set_events = utils.deduplication(row_data)
        if set_events is None:
            print("Events is None, deduplication problem")
            return
            
        list_events = list(set_events)

        formatted_events = []
        for i in range(len(list_events)):
            splice_global = list_events[i][1].find("Global:") # why row_data[i][1]? Because [1] is where the date is stored. It's usually
                                                           # "EVENT_NAME | CN:2025-12-23GLOBAL:2026-5-23" so we have to get the [1] for the date.
            if splice_global != -1:
                global_date = list_events[i][1][splice_global:]
            event_info = (f"Event {i+1}: {list_events[i][0]} | Date: {global_date}")
            formatted_events.append(event_info)
        formatted_events = list(dict.fromkeys(formatted_events))
        return formatted_events
            
    def data_getter(self):
        site_config = self.sites[0]
        table, url, game = site_config
        response = self.get_response(url)
        events = self.find_arknights_events(response, table, game, self.dates)
        data = self.format_arknights(events)
        return data
    