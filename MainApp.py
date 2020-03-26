from Qscraper import ScrapeHandler

# This code was made for python 2 and will NOT work for python 3

# my_Scraper object create from the ScrapeHandler class located in the Qscraper
# file. Object initialized with the date in order to name the resulting csv file
my_Scraper = ScrapeHandler()
# my_Scraper calculatedPhonePrices and creates a csv file with appropriate
# information. Csv file used as reference by a chat bot for buying used phones.
my_Scraper.calculatePhonePrices()
# information collected added to a database file
my_Scraper.addToDataBase()
