from Qscraper import ScrapeHandler

# This code was made for python 2 and will NOT work for python 3


my_Scraper = ScrapeHandler()
# my_Scraper calculatedPhonePrices and creates a csv file with appropriate
# information. Csv file used as reference by a chat bot for buying used phones.
my_Scraper.calculatePhonePrices()
# information collected added to a database file
my_Scraper.addToDataBase()
