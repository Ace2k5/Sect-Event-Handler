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
        while True:
            for i in range(len(sites)):
                soup = self.get_response(sites[i][1])
                self.findTables(soup, sites[i][0], sites[i][2], dates)
            break
            
    def get_response(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                return soup
        except requests.exceptions.RequestException as e:
            print(f"Problem appeared as {e}")
            return None
                
    
    def findTables(self, soup, table_text, game_name, date_formats):
        if soup is None:
            print("No HTML content to parse!")
            return
        
        events = soup.find_all("table", class_=table_text)
        print(f"Currently in {game_name}")
        for table in events:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if cells:
                    row_data = []
                    for cell in cells:
                        text = cell.get_text(strip=True)
                        row_data.append(text)
                    row_text = ' | '.join(row_data)
                    for date_format in date_formats:
                        if date_format in row_text:
                            print(f"Event Date: {row_text}")
                            break


a = WebScraper()