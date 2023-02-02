import os
import logging

import scrapy
from scrapy.crawler import CrawlerProcess

class HotelSpider(scrapy.Spider): #the spider is launching the request
    # Name of spider
    name = 'hotel'

    # Starting URL
    start_urls = [
        'https://www.booking.com/'
        ]

    # Parse function =entry point of the spider to browse in the form request of the cities, based on the txt file containing the list of cities:
    def parse(self, response):
        file = open('/Users/elisa/Documents/3-Formation_Elisa/Jedha/2022-10_Fullstack/03-Data_collection/KAYAK/cities.txt', 'r')
        cities = file.readlines()
        for cit in cities:
            yield scrapy.FormRequest.from_response( #return scrapy.FormRequest.from_response(
                response,
                formdata={'ss': cit}, # ss is the name given to city field on the main page of booking
                callback=self.after_search #after_search defined below
                )

    # Callback above defined: 
    def after_search(self, response):
        for path in response.xpath('//*[@data-testid="property-card"]') : #path of the property card of each hotel on booking

            # xpath of each items
            city = path.xpath('//*[@id="right"]/div[1]/div/div/div/h1/text()').get()
            name =  path.xpath('div[1]/div[2]/div/div/div[1]/div/div[1]/div/h3/a/div[1]/text()').get()
            rating = path.xpath('div[1]/div[2]/div/div/div[2]/div[1]/a/span/div/div[1]/text()').get()
            desc = path.xpath('div[1]/div[2]/div/div/div[1]/div/div[3]/text()').get()
            url = path.xpath('div[1]/div[2]/div/div/div[1]/div/div[1]/div/h3/a').attrib["href"]

            # put all together in a dictionnary:
            dic = {'city': city,
                'name': name,
                'rating' : rating,
                'desc' : desc,
                'url': url
                }

            # initiate method for the parse_hotel GPS cordonnates 
            try: 
                yield response.follow(url = url, # yield allows to work in sequence; waits for the GPS function described below
                                    callback = self.GPS, 
                                    cb_kwargs = {'dic': dic}
                                    ) 
            except: # gives error in case not all items from dictionnary are properly gathered
                yield dic
                print('error')
                
    def GPS(self, response, dic):
        try:
            coord = response.css('a.jq_tooltip.loc_block_link_underline_fix.bui-link.show_on_map_hp_link.show_map_hp_link').attrib['data-atlas-latlng']
            dic['gps'] = coord # adding new key in dic
            yield dic
        except:
            yield dic
            print('error')

# Name of the file where the results will be saved
filename = "hotel_details.json"

# If file already exists, delete it before crawling (because Scrapy will concatenate the last and new results otherwise)
if filename in os.listdir('src/'):
        os.remove('src/' + filename)

# Declare a new CrawlerProcess with some settings
process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        'src/' + filename: {"format": "json"},
    }
})

# Start the crawling using the spider defined above
process.crawl(HotelSpider)
process.start()    