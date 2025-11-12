import requests
from bs4 import BeautifulSoup
from datetime import date
import inits, get_time

class WebScraper():
    def __init__(self):
        sites = inits.SITES # (TABLE CLASS, URL, GAME)
        dates = get_time.getTime()
        self.flow(sites, dates)
    
    def flow(self, sites, dates):
        '''
        Args:
            sites: a list containing tuples of relevant strings to each individual game ('HTML class', 'URL link', 'Game Name')
            dates: a list containing multiple formats of yyyy-mm-dd
        
        This function is the main flow of the web scraper. Everything web scraping related must be implemented here.
        '''
        # Arknights
        soup = self.get_response(sites[0][1])
        data = self.find_arknights_events(soup, sites[0][0], sites[0][2], dates)
        if len(data) > 1:
            self.format_arknights(data)
        else:
            print("Something went wrong with trying to get data from Arknights")
        # Limbus Company
        
            
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
            return
                        
    
    def format_arknights(self, row_data):
        '''
        Args:
            row_data: A list containing each events found in Arknights by a pair of strings
            
        The goal of this function is to format the extracted events info in Arknights.
        '''
        print(row_data)
        for i in range(len(row_data)):
            splice_global = row_data[i][1].find("Global:")
            if splice_global != -1:
                global_date = row_data[i][1][splice_global:]
            print(f"Event: {row_data[i][0]} | Date: {global_date}")
    #############################################################################################################################
    
    # Limbus Company
    
    

a = WebScraper()