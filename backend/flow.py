from .games_wiki import arknights, limbus, base_webhook
from . import json_handler, logger, utils
from functools import partial

class ScrapeFlow():
    def __init__(self, signals=None):
        self.logger = logger.Log(signals=signals)
        if not json_handler.JSON_FILE.exists():
            json_handler.create_user_data(self.logger)
        self.ark_scrape = arknights.ArkScraper(self.logger)
        self.limbus = limbus.LimbusScraper(self.logger)
        self.send = partial(base_webhook.send_to_discord, logger=self.logger)
        self.webhook = partial(utils.get_webhook, user=json_handler.get_user_data(), logger=self.logger)

    def test(self):
        if not self.webhook("Limbus Company"):
            self.logger.log_error("User does not have a valid webhook URL for Limbus Company.")
            return
        else:
            datas = self.limbus.data_getter()
            self.send(datas, "Limbus Company")
        if not self.webhook("Arknights"):
            self.logger.log_error("User does not have a valid webhook URL for Arknights.")
        else:
            datas = self.ark_scrape.data_getter()
            self.send(datas, "Arknights")



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
                if not self.webhook("Arknights"):
                    self.logger.log_error("Local files does not have a valid webhook URL for Arknights. Skipping Arknights.")
                else:
                    datas = self.ark_scrape.data_getter()
                    if datas is None:
                        self.logger.log_error("Nothing was returned, skipping Arknights...")
                    self.send(datas, "Arknights")
                
                if not self.webhook("Limbus Company"):
                    self.logger.log_error("Local files does not have a valid webhook URL for Limbus Company. Skipping Limbus Company.")
                else:
                    datas = self.limbus.data_getter()
                    if datas is None:
                        self.logger.log_error("Nothing was returned, skipping Limbus Company...")
                    self.send(datas, "Limbus Company")
            else:
                pass # check_date has a c
            self.logger.log_info("Done.")
        except Exception:
            self.logger.log_error("A failure has occured.")
        
if __name__ == "__main__":
    runner = ScrapeFlow()
    check = int(input("Check GUI (1) Test program (2):"))
    if check == 1:
        runner.flow()
    elif check == 2:
        runner.test()