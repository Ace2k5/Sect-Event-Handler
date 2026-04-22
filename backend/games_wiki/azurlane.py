import requests
from .base_scraper import BaseScraper
from bs4 import BeautifulSoup
from datetime import date
from .. import backend_inits, utils
from urllib.parse import urljoin
# Azur Lane wiki is protected by Anubis, and I cannot find an alternative.
class AzurLaneScraper(BaseScraper):
    def __init__(self, logger, user_data=None, headers=None):
        name = "Azur Lane"
        super().__init__(name_of_game=name, logger=logger, user_data=user_data, headers=headers)
        self.logger = logger
        self.game = self.user_data["Azur Lane"]
        
    def find_events(self, soup, table_class, game):
        if soup is None:
            self.logger.log_error(f"Soup is none in Azur Lane.")
            return
        found_events = []
        self.logger.log_info("Currently in Azur Lane.")
        events = soup.find_all("table", class_="evt-list-tbl")
        if not events:
            print("No events")
        print(found_events)
        print(soup.prettify())
    def format_events(self, row_data):
        pass
    
    def data_getter(self, forced=False):
        try:
            if self.game["webhook"].startswith("https"):
                site_config = self.sites[2]
                table, url = site_config
                soup = self.get_response(url)
                if soup is None:
                    raise ValueError("Could not get HTML data in BaseScraper get_response function.")
                self.find_events(soup, url, table)
                
            else:
                self.logger.log_error("Azur Lane does not have a valid URL in the local files.")
                return None
        except Exception as e:
            self.logger.log_error(f"Error occured as {e} in Azur Lane")
        finally:
            self.session.close()