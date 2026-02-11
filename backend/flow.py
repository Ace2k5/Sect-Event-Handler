from .games_wiki import arknights, limbus, arknights_webhook
from . import json_handler, logger

class ScrapeFlow():
    def __init__(self):
        self.logger = logger.Log()
        ark_scrape = arknights.ArkScraper(self.logger)
        self.flow(self.logger, ark_scrape)
        
    def flow(self, logger, ark):
        '''
        Args:
            ark: object of ArkScraper
        
        This function is the main flow of the web scraper. Everything web scraping related must be implemented here.
        '''
        # Arknights
        '''current_date = json_handler.check_date()
        if not current_date:'''
        data = ark.data_getter()
        arknights_webhook.send_to_discord(logger, data)
        for i in data:
            logger.info(f"Event Name: {i['Event']} | CN: {i['CN']} | Global: {i['Global']}")
        else:
            pass