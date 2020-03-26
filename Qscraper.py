import requests         # requests must be locally installed (using pip)
from lxml import html   # lxml must be locally installed (using pip)
import csv              # csv comes with python 2 and 3.
from datetime import date

class ScrapeHandler(object):
    def __init__(self):
        # phone_means dictonary defined after parsing eBay's sold phones webpage
        self.phone_means = {}
        # phones dictionary has a naming convention for each phone that must be
        # followed. Example: CompanyName_ModelNumber_Storage_Carrier
        # The eBay link must be to recently sold phones.
        self.phones = {
            'Apple_X_256_att': 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=iphone+x+256+att&_sacat=0&_dmd=1&_prodsch=0&LH_All=1&_sop=12&rt=nc&LH_Sold=1&LH_Complete=1',
            'Apple_X_256_verizon': 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=iphone+x+256+verizon&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1',
            'Apple_8_256_verizon': 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=iphone+8&_sacat=0&Network=Verizon&Storage%2520Capacity=256%2520GB&_dcat=9355&rt=nc&LH_Sold=1&LH_Complete=1',
            }

    def calculatePhonePrices(self):
        # for loop calls calPhoneMean for each phone in the phone dictonary.
        for key, value in self.phones.items():
            key_mean = self.calPhoneMean(value)
            print(key + "'s average price is: " + str(key_mean))
            self.phone_means[key] = key_mean
            print('***************************************')
        # once data has been collected a csv file is created.
        self.createCSV()

    def calPhoneMean(self, url):
        total = 0
        num_phones = 0
        mean = 0
        # bn2 stands for bought numbers 2 as list hold refined integer prices
        bn2 = []
        r = requests.get(url)
        tree = html.fromstring(r.content)
        phone_prices = []
        phone_prices = tree.xpath("//span[@class='POSITIVE']/text()")
        #print(phone_prices) # Prints array of unpared phone prices.
        for x in phone_prices:
            y = x.replace('$', '')
            temp = y.split('.')
            y = temp[0]
            if (len(y) > 3):
                y = y.replace(',', '')
            int_y = int(y)
            bn2.append(int_y)
            num_phones += 1

        for i in bn2:
            try:
                total += i
            except:
                print("Total integer too large at index: " + i)
        # try except block used to ensure if the total gets to large or small
        # for a specific phone other phones can still be researched.
        try:
            mean = total / num_phones
        except:
            print "Mean could not be calculated."

        # Print to used number of phones used to arrive at the mean.
        print("Total number of phones: " + str(num_phones))
        return mean

    def createCSV(self):
        # Multipliers used for creating appropriate used phone offers.
        perfectMultiplier = 0.6
        goodMultiplier = 0.5
        poorMultiplier = 0.2
        # file_name sets the name of the generated csv file.
        file_name =  'qphones.csv'
        # csv opened and rewritten or created.
        with open(file_name, 'w') as csv_file:
            writer = csv.writer(csv_file)
            column = ['Make', 'Model', 'Carrier', 'Size', 'eBay Average', 'Perfect Multiplier', 'Perfect Cubert Price', 'Good Multiplier', 'Good Cubert Price', 'Poor Multiplier', 'Poor Cubert Price', 'Landbot Code']
            writer.writerow(column)
            # for loop used to write a new line for each phone's data.
            for key, value in self.phone_means.items():
                value_int = int(value)
                temp = key.split('_')
                row = [temp[0], temp[1], temp[3], temp[2], value, perfectMultiplier, (value_int * perfectMultiplier), goodMultiplier, (value_int * goodMultiplier), poorMultiplier, (value_int * poorMultiplier), key]
                writer.writerow(row)
        # print to user message
        print("End of createCSV function.")

    def addToDataBase(self):
        # database.csv must have been created before this is run
        db_name = 'database.csv'
        today = str(date.today())
        # csv file is opened and data is added
        with open(db_name, 'a') as database_file:
            writer = csv.writer(database_file)
            for key, value in self.phone_means.items():
                temp = key.split('_')
                db_row = [today, key, value, temp[0], temp[1], temp[3], temp[2]]
                writer.writerow(db_row)
