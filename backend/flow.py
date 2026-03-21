from .games_wiki import arknights, limbus, base_webhook
from . import json_handler, logger, utils
from functools import partial

class ScrapeFlow():
    """
    Main controller class that orchestrates web scraping and Discord notification flow.
    
    This class manages the complete workflow:
    1. Initializes logging and configuration
    2. Creates game-specific scraper instances
    3. Coordinates scraping of multiple game wikis
    4. Sends formatted event data to Discord webhooks
    
    Attributes:
        logger: Custom Log instance for logging messages
        ark_scrape: ArkScraper instance for Arknights wiki scraping
        limbus: LimbusScraper instance for Limbus Company wiki scraping
        send: Partial function for sending data to Discord webhooks
        webhook: Partial function for retrieving webhook URLs from configuration
    """
    def __init__(self, signals=None):
        """
        Initializes the ScrapeFlow controller.
        
        Args:
            signals: Optional signals object for GUI communication (PySide6 signals)
            
        Notes:
            - Creates user configuration file if it doesn't exist
            - Initializes game scraper instances
            - Sets up partial functions for webhook operations
        """
        self.logger = logger.Log(signals=signals)
        if not json_handler.JSON_FILE.exists():
            json_handler.create_user_data(self.logger)
        self.ark_scrape = arknights.ArkScraper(self.logger)
        self.limbus = limbus.LimbusScraper(self.logger)
        self.send = partial(base_webhook.send_to_discord, logger=self.logger)
        self.webhook = partial(utils.get_webhook, user=json_handler.get_user_data(), logger=self.logger)

    def test(self):
        """
        Test method for development and debugging.
        
        Performs a test scrape of Arknights events and sends to Discord.
        Useful for verifying scraping functionality without running full flow.
        
        Returns:
            None: Sends test data directly to Discord webhook if events found
        """
        datas = self.ark_scrape.data_getter()
        if not datas or datas is None:
            self.logger.log_info("There are no new events.")
        else:
            self.send(datas, "Arknights")
        datas = self.limbus.data_getter()
        if not datas or datas is None:
            self.logger.log_info("There are no new events.")
        else:
            self.send(datas, "Limbus Company")



    def flow(self, forced=False):
        """
        Main execution flow for the web scraper.
        
        Orchestrates the complete scraping and notification process:
        1. Checks if date has changed (prevents duplicate daily runs)
        2. For each supported game:
           - Retrieves webhook URL from configuration
           - Scrapes game wiki for events
           - Filters and formats event data
           - Sends notifications to Discord webhook
        3. Logs completion or errors
        
        Args:`
            forced: If True, forces execution regardless of date check.
                   Used for manual triggering from GUI vs scheduled runs.
            
        Returns:
            None: Sends data directly to Discord webhooks, logs results
            
        Notes:
            - Only runs if date has changed since last run (unless forced)
            - Skips games without valid webhook URLs
            - Continues with next game if one fails
        """
        try:
            check_date = json_handler.check_date(self.logger) # False if date is not up to date, else true
            if not check_date or forced:
            # Arknights
                if not self.webhook("Arknights"):
                    self.logger.log_error("Local files does not have a valid webhook URL for Arknights. Skipping Arknights.")
                else:
                    print(forced)
                    datas = self.ark_scrape.data_getter(forced)
                    if datas is None:
                        self.logger.log_error("Nothing was returned, skipping Arknights...")
                    self.send(datas, "Arknights")
                
                if not self.webhook("Limbus Company"):
                    self.logger.log_error("Local files does not have a valid webhook URL for Limbus Company. Skipping Limbus Company.")
                else:
                    datas = self.limbus.data_getter(forced)
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