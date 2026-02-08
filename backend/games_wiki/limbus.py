import requests
from .base_scraper import BaseScraper
from bs4 import BeautifulSoup
from datetime import date
from .. import inits, utils

class LimbusScraper(BaseScraper):
    def find_events(self, soup, table_class, game, dates_format) -> list:
        '''
            Args:
                soup: parser for the URL
                table_class: HTML class
                game_name: Name of the game
                date_formats: a list containing multiple formats of yyyy-mm-dd
                
            returns:
                A list containing all of the events inside the Limbus Wiki
            
        '''
        
        if game == "Limbus Company":
            
            if soup is None:
                print("Soup is none in Limbus Company")
                return
            # November 2025 turns into:
            target_month = dates_format.split()[0] # November 
            target_year = dates_format.split()[1] # 2025
            
            found_events = []
            print(f"Currently in {game}")
            events = soup.find_all("table", class_=table_class)
            for table in events: # iterates everything inside the table_class
                rows = table.find_all("tr")
                for row in rows: # delves deeper into tr
                    cells = row.find_all("td") # gets string from td
                    if cells:
                        row_data = []
                        for cell in cells:
                            text = cell.get_text(strip=True) # remove unnecessary text
                            row_data.append(text)
                        if len(row_data) > 1 and target_month in row_data[1] and target_year in row_data[1]: # protect against single elements and for current date and year.
                            found_events.append(row_data)
            return found_events

    def format_events(self, row_data) -> list:
        '''
        Args:
            row_data: A list of events which contains the substrings of current date
            
        Format Limbus Company events by deduplicating, cleaning empty strings, 
        and formatting into readable strings.
    
        Table structure is guaranteed: [Event Name, Start Date, End Date]

        returns:
            A clean list that contains [Event Name, Start Date, End Date]
        '''
        if row_data is None:
            print("Row data is None on Limbus")
            return
        
        # deduplication
        events = utils.deduplication(row_data)
        if events is None:
            print("Events is None, deduplication problem")
            return
        
        # trim empty strings
        list_events = list(events)
        clean_list = utils.trimEmptyString(list_events)
            
        formatted_events = []
        for i in range(len(clean_list)):
            if len(clean_list[i]) >= 3:
                event_info = (f"Event {i+1}: {clean_list[i][0]} | Date: {clean_list[i][1]} - {clean_list[i][2]}")
                formatted_events.append(event_info)
        if not formatted_events:
            print("No ongoing events in Limbus Company.")
            return None
        
        return formatted_events
    
    def data_getter(self) -> list:
        site_config = self.sites[1]
        table_class, url, game = site_config
        soup = self.get_response(url)
        data = self.find_events(soup, table_class, game, self.dates[0])
        if data is None:
            return None
        formatted_data = self.format_events(data)
        return formatted_data
        
        
        
a = LimbusScraper()