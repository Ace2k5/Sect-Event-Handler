from .games_wiki import arknights, limbus, arknights_webhook
from . import json_handler, logger

class ScrapeFlow():
    def __init__(self):
        self.logger = logger.Log()
        ark_scrape = arknights.ArkScraper(self.logger)
        self.flow(self.logger, ark_scrape)
        
    def flow(self, logger, ark):
        '''
        Main execution flow for the web scraper.
        
        Args:
            logger: Log object for logging messages
            ark: ArkScraper object for fetching event data
            
        Returns:
            None: Sends data directly to Discord webhook
        '''
        # Arknights
        data = ark.data_getter()
        arknights_webhook.send_to_discord(logger, data)
        for i in data:
            logger.info(f"Event Name: {i['Event']} | CN: {i['CN']} | Global: {i['Global']}")