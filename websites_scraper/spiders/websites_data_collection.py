import time

import scrapy
import logging
import concurrent.futures
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


class WebsitesDataCollectionSpider(scrapy.Spider):
    def __init__(self, input_url=None, **kwargs):
        super().__init__(**kwargs)
        if input_url is None:
            input_url = ['https://docs.scrapy.org/en/latest/intro/tutorial.html#our-first-spider',
                         'https://stackoverflow.com/questions/53733190/is-scrapy-compatible-with-multiprocessing',
                         'https://www.illion.com.au/contact-us/',
                         'https://www.oakley.com', 'https://www.latimes.com', 'https://www.dmoz.org',
                         'https://www.msu.edu', 'https://www.yahoo.com', 'https://www.auda.org.au']
        self._input_url = input_url

    name = "websites_data_collection"
    allowed_domains = ["www.illion.com.au"]
    start_urls = ["http://www.illion.com.au/"]

    def start_requests(self):
        print(self._input_url)
        if isinstance(self._input_url, list):
            for url_to_scrape in self._input_url:
                print('aaa')
                yield scrapy.Request(url=url_to_scrape, callback=self.parse)
        else:
            yield scrapy.Request(url=self._input_url, callback=self.parse)

    def parse(self, response, **kwargs):
        print('COLLECTING>> ', response.url)
        yield {'url_collected': response.url}
