from .games_wiki import arknights, arknights_webhook
from . import json_handler, logger

class ScrapeFlow():
    def __init__(self, window=None):
        self.window = window
        self.logger = logger.Log()
        self.ark_scrape = arknights.ArkScraper(self.logger, window=self.window)
        
    def flow(self, forced=False):
        '''
        Main execution flow for the web scraper.
        
        Args:
            forced=False: helps manage between task scheduler and GUI
            
        Returns:
            None: Sends data directly to Discord webhook
        '''
        check_date = json_handler.check_date(self.logger) # False if date is not up to date, else true
        try:
            if not check_date or forced:
            # Arknights
                datas = self.ark_scrape.data_getter()
                arknights_webhook.send_to_discord(self.logger, datas)
                for data in datas:
                    self.logger.log_info(f"Event Name: {data['Event']} | CN: {data['CN']} | Global: {data['Global']}")   
        except Exception:
            self.logger.log_error("A failure has occured.")
        
if __name__ == "__main__": # for windows task scheduler
    runner = ScrapeFlow()
    runner.flow(forced=False)