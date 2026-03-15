from .games_wiki import arknights, arknights_webhook, limbus, limbus_webhook
from . import json_handler, logger

class ScrapeFlow():
    def __init__(self, signals=None):
        self.logger = logger.Log(signals=signals)
        if not json_handler.JSON_FILE.exists():
            json_handler.create_user_data(self.logger)
        self.ark_scrape = arknights.ArkScraper(self.logger)
        self.limbus = limbus.LimbusScraper(self.logger)    

    def test(self):
        user = json_handler.get_user_data()
        if not user["limbus"]["webhook"].startswith("https"):
            self.logger.log_error("User does not have a valid webhook URL for Limbus Company.")
            return
        else:
            datas = self.limbus.data_getter()
            limbus_webhook.send_to_discord(self.logger, datas)
            return datas


    def flow(self, forced=False):
        '''
        Main execution flow for the web scraper.
        
        Args:
            forced=False: helps manage between task scheduler and GUI
            
        Returns:
            None: Sends data directly to Discord webhook
        '''
        try:
            check_date = json_handler.check_date(self.logger) # False if date is not up to date, else true
            if not check_date or forced:
            # Arknights
                datas = self.ark_scrape.data_getter()
                arknights_webhook.send_to_discord(self.logger, datas)


                for data in datas:
                    self.logger.log_info(f"Event Name: {data['Event']} | CN: {data['CN']} | Global: {data['Global']}")
        except Exception:
            self.logger.log_error("A failure has occured.")
        
if __name__ == "__main__":
    runner = ScrapeFlow()
    s = runner.ark_scrape.data_getter()
    arknights_webhook.send_to_discord(runner.logger, s)