from .games_wiki import arknights, limbus, arknights_webhook
from . import json_handler

class ScrapeFlow():
    def __init__(self):
        ark_scrape = arknights.ArkScraper()
        self.flow(ark_scrape)
        
    def flow(self, ark):
        '''
        Args:
            ark: object of ArkScraper
        
        This function is the main flow of the web scraper. Everything web scraping related must be implemented here.
        '''
        # Arknights
        '''current_date = json_handler.check_date()
        if not current_date:'''
        data = ark.data_getter()
        arknights_webhook.send_to_discord(data)
        for i in data:
            print(f"Event Name: {i['Event']} | CN: {i['CN']} | Global: {i['Global']}")
        else:
            pass