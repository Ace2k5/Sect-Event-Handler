import requests
from .base_scraper import BaseScraper
from bs4 import BeautifulSoup
from datetime import date
from .. import inits, get_time, utils
from pathlib import Path
import json
from urllib.parse import urljoin

class ArkScraper(BaseScraper):
    def __init__(self):
        self.sites = inits.SITES # (TABLE CLASS, URL, GAME)

    # Arknights ###################################################################################################################
    def find_events(self, soup, table_text, game_name):
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
                        
    def find_img(self, soup, url, table_class, game):
        if game != "Arknights":
            print("The game args is not Arknights, please fix.")        
        else:
            filepath = Path("./arknights_imgs/")
            filepath.mkdir(parents=True, exist_ok=True)
            saved_event_imgs = list()
            for img in soup.find_all("img", class_=table_class):
                img_url = urljoin(url, img["src"])
                filename = img["alt"]
                data = requests.get(img_url).content

                text = filename
                if "CN" in text:
                    text_part_temp = text.split("CN", 1)[1].strip()
                elif "EN" in text:
                    text_part_temp = text.split("EN", 1)[1].strip()
                else:
                    text_part_temp = text.strip()
                text_part = text_part_temp.split("banner")[0].strip() if "banner" in text_part_temp else text_part_temp.split(".png")[0]

                save_path = filepath / (text_part + ".png")

                with open(save_path, "wb") as file:
                    file.write(data)
                saved_event_imgs.append({
                    "Image_Name": text_part,
                    "Image_URL": img_url
                })
            return saved_event_imgs

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
            else:
                print(f"Could not normalize CN date in {date_str}")
                return None

            global_date = None
            if "Global:" in date_str:
                global_date_part = date_str.split("Global:")[1]
                global_date = global_date_part.split("(")[0].strip()
                normalized_global = utils.normalize_date_range(global_date)
            else:
                print(f"Could not normalize Global date in {date_str}")
                return None

            clean_format.append({
                "Event": event_name,
                "CN": normalized_cn,
                "Global": normalized_global
            })
        return clean_format
    
    def link_imgs(self, dictionary_of_events: dict[str, str], list_of_imgs: list[str]):
        for event in dictionary_of_events:
            event_name = event["Event"].replace(":", "").replace("-", "").replace("_", "")
            for imgs in list_of_imgs:
                print(f"{imgs["Image_Name"]}, {imgs["Image_URL"]}")
                if imgs["Image_Name"] in event_name:
                    event["Event_PNG"] = imgs["Image_Name"]
                    event["Event_PNG_URL"] = imgs["Image_URL"]

                    print(f"Added {event["Event_PNG_URL"]} to {event["Event_PNG"]}")
        return dictionary_of_events

            
    def data_getter(self):
        site_config = self.sites[0]
        table, url, game = site_config
        soup = self.get_response(url)
        events = self.find_events(soup, table, game)
        data = self.format_events(events)
        imgs_name = self.find_img(soup, url, "banner", game)

        formatted_data = self.link_imgs(data, imgs_name)
        print(formatted_data)
        return formatted_data
    