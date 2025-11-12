from .games import arknights

class ScrapeFlow():
    def __init__(self):
        ark_scrape = arknights.ArkScraper()
        self.flow(ark_scrape)
        
    def flow(self, ark):
        '''
        Args:
            sites: a list containing tuples of relevant strings to each individual game ('HTML class', 'URL link', 'Game Name')
            dates: a list containing multiple formats of yyyy-mm-dd
        
        This function is the main flow of the web scraper. Everything web scraping related must be implemented here.
        '''
        # Arknights
        try:
            data = ark.data_getter()
            for i in range(len(data)):
                print(data[i])
        except Exception as e:
            print(f"Error occured as {e}")
            
            
            
            
a = ScrapeFlow()