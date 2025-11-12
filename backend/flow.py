from .games import arknights, limbus

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
            for i in range(len(data)):
                print(data[i])
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