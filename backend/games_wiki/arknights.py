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
    def find_events(self, soup, table_text, game_name):
        '''
        searches tables for the events
        
        Args:
            soup: BeautifulSoup parser object for the URL HTML content
            table_text: CSS class name of the HTML table to search for
            game_name: Name of the game (e.g., "Arknights")
            
        Returns:
            List of lists containing event data: [event_name, date_string, ...]
        '''
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
                        print(f"Appending {text} to row_data...")
                        row_data.append(text)
                        if len(row_data) > 1:
                            found_events.append(row_data)
        return found_events
                        
    def find_img(self, soup: BeautifulSoup, url: str, table_class: str, game: str) -> list[dict]:
        '''
        downloads images for local use and saves img url in case we need to request the image again
        
        Args:
            soup: BeautifulSoup parser object
            url: url of the game for img
            table_class: CSS class name of images to find
            game: Name of the game
            
        Returns:
            List of dictionaries with structure:
            [
                {
                    "Image_Name": str (cleaned filename without extension),
                    "Image_URL": str (full URL to the image)
                },
                ...
            ]
        '''
        filepath = Path("./arknights_imgs/")
        filepath.mkdir(parents=True, exist_ok=True)
        saved_event_imgs = list()
        
        for img in soup.find_all("img", class_=table_class):
            img_url = urljoin(url, img["src"])
            filename = img["alt"]
            response = self.session.get(img_url)
            if not utils.request_error_handling(response):
                print(f"Could not get image {img}. find_img function.")
                continue
            data = response.content
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
        lookbackdays = self.user_data('lookback_days', 30)
        set_events = utils.deduplication(row_data)
        if set_events is None:
            raise ValueError("Expected a set, None was returned.")
            
        list_events = list(set_events)

        clean_format = []

        for row in list_events:
            event_name = row[0]
            date_str = row[1]

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
                "Global": normalized_global
            })
        return clean_format
    
    def link_imgs(self, dictionary_of_events: list[dict], list_of_imgs: list[dict]) -> list[dict]:
        '''
        links event and imgs by using substring match then append into existing dictionary(dictionary_of_events)
        Args:
            dictionary_of_events (list of dict):
                {
                    "Event": str (event name),
                    "CN": str (CN date range (DATE ONLY)),
                    "Global": str (Global date range (DATE ONLY))
                }
                
            list_of_imgs (list of dict):
                {
                    "Image_Name": str (cleaned image filename),
                    "Image_URL": str (URL to the image)
                }
                    
        Returns:
            adds new keys inside of dictionary_of_events:
                "Event_PNG": str (image filename)
                "Event_PNG_URL": str (image URL)
        '''
        
        for event in dictionary_of_events:
            print(f"Current event: {event['Event']}")
            event_name = event["Event"].replace(":", "").replace("-", "").replace("_", "")
            matched = False
            for imgs in list_of_imgs:
                print(f"Matching {imgs['Image_Name']} to {event_name}")
                if imgs["Image_Name"] in event_name:
                    event["Event_PNG"] = imgs["Image_Name"]
                    event["Event_PNG_URL"] = imgs["Image_URL"]
                    matched = True
                    print(f"Matched {imgs['Image_Name']} to {event_name}.")
                    print(f"Saved as: {event['Event_PNG']} and {event['Event_PNG_URL']}")
                    break
            if not matched:
                print(f"No images linked with {event['Event']}")
        return dictionary_of_events

            
    def data_getter(self):
        '''    
        Returns:
            List of dictionaries with complete event information:
            [
                {
                    "Matched_Event_IMGS": dict (matched event metadata),
                    "CN_Date": str (CN release date range (DATE ONLY)),
                    "Global_Date": str (Global release date range (DATE ONLY)),
                    "Image_URL": str (URL to event banner image)
                },
                ...
            ]
        '''
        try:
            site_config = self.sites[0]
            table, url, game = site_config
            soup = self.get_response(url)
            if soup is None:
                raise ValueError("Could not get HTML data in BaseScraper get_response function.")
            
            events = self.find_events(soup, table, game)
            data = self.format_events(events)
            imgs_list = self.find_img(soup, url, "banner", game)
            formatted_data = self.link_imgs(data, imgs_list)
            return formatted_data
        except Exception:
            raise
        finally:
            self.session.close()