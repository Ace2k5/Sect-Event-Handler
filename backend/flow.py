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
        check_date = json_handler.check_date(logger) # False if date is not up to date, else true
        try:
            #if not check_date:
            # Arknights
                datas = ark.data_getter()
                arknights_webhook.send_to_discord(logger, datas)
                for data in datas:
                    logger.log_info(f"Event Name: {data['Event']} | CN: {data['CN']} | Global: {data['Global']}")   
        except Exception:
            self.logger.log_error("A failure has occured.")
        
a = ScrapeFlow()