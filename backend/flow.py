from .games_wiki import arknights, limbus, arknights_webhook

class ScrapeFlow():
    def __init__(self):
        ark_scrape = arknights.ArkScraper()
        limbus_scrape = limbus.LimbusScraper()
        self.flow(ark_scrape, limbus_scrape)
        
    def flow(self, ark, limbus):
        '''
        Args:
            ark: object of ArkScraper
        
        This function is the main flow of the web scraper. Everything web scraping related must be implemented here.
        '''
        # Arknights
        try:
            data = ark.data_getter()
            arknights_webhook.send_to_discord(data, "???")
            for i in data:
                print(f"Event Name: {i['Event']} | CN: {i['CN']} | Global: {i['Global']}")
        except Exception as e:
            print(f"Error occured as {e}")
        # Limbus
        try:
            data = limbus.data_getter()
            for i in range(len(data)):
                print(data[i])
            
        except Exception as e:
            print(f"Error occured as {e}")
            
a = ScrapeFlow()