import requests
from bs4 import BeautifulSoup
from datetime import date
from .. import inits, get_time, utils

class LimbusScraper():
    def __init__(self):
        self.sites = inits.SITES
        self.dates = get_time.getTime()
        
    
    def get_response(self, url):
        '''
        Args:
            url: Contained inside of a tuple located in inits.py, the 3rd iteration.
        
        '''
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                return soup
            else:
                print(f"Response status ended up being: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error occured as {e}")
            return None
        
    def find_limbus_events(self, soup, table_class, url, game, dates_format):
        '''
            Args:
                soup: parser for the URL
                table_text: HTML class
                game_name: Name of the game
                date_formats: a list containing multiple formats of yyyy-mm-dd
                
            The goal of this function is to find the current events inside of the Limbus Company Wiki.
            
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
                        if target_month in text and target_year in text:
                            found_events.append(row_data)
            return found_events
                            
                
    def format_limbus(self, row_data):
        '''
        Args:
            row_data: A list of events which contains the substrings of current date
            
        Format Limbus Company events by deduplicating, cleaning empty strings, 
        and formatting into readable strings.
    
        Table structure is guaranteed: [Event Name, Start Date, End Date]
        '''
        if row_data is None:
            print("Row data is None on Limbus")
            return
        
        # deduplication
        events = utils.deduplication(row_data)
        
        # trim empty strings
        list_events = list(events)
        clean_list = utils.trimEmptyString(list_events)
            
        formatted_events = []
        for i in range(len(clean_list)):
            event_info = (f"Event {i+1}: {clean_list[i][0]} | Date: {clean_list[i][1]} - {clean_list[i][2]}")
            formatted_events.append(event_info)
        return formatted_events
        
            
        
    
    def data_getter(self):
        site_config = self.sites[1]
        table_class, url, game = site_config
        soup = self.get_response(url)
        data = self.find_limbus_events(soup, table_class, url, game, self.dates[0])
        formatted_data = self.format_limbus(data)
        return formatted_data
        
        
        
a = LimbusScraper()