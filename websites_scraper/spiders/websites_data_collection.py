import re
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
    start_urls = ["https://support.google.com/business/answer/7690269?hl=en"]

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
        parsed_url = response.url
        website_html = response.body
        print(website_html)
        logo_url = response.css('img[src*=logo]::attr(src)').get()

        phone_numbers = []

        # Coletar todos os números de telefone usando regex
        phone_regex = r'\+?\d{1,3}[-.\s]?\(?\d{2,}\)?[-.\s]?\d{4}[-.\s]?\d{4}'
        phone_regex = r'\+?\d{1,3}[-.\s]?\(?\d{2,}\)?[-.\s]?\d{4}[-.\s]?\d{4}'
        phone_regex = r'(?:\+[\d-]+)?\s*(?:\([\d-]+\)|[\d-]+)(?:\s*(?:ext\.?|\bex)?\s*[\d-]+)*'
        # phone_regex = "^\\+?\\d{1,4}?[-.\\s]?\\(?\\d{1,3}?\\)?[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,9}$"
        #phone_numbers = re.findall(phone_regex, response.text)

        brazilian_phone_pattern = r"\+55\s*\d{2}\s*(?:\d{4,5}[-\s]?\d{4}|\d{8})"
        brazilian_phone_pattern = r"(?:\+?\d{1,3}[- ]?)?\(?\d{2,3}\)?[- ]?\d{4,5}[- ]?\d{4}"
        brazilian_numbers = re.findall(brazilian_phone_pattern, response.text)

        phone_numbers = phone_numbers + brazilian_numbers

        us_phone_pattern = r"(?:^|\s)(((?:\+|0{2})(?:49|43|33)[-\. ]?|0)([1-9]\d{1,2}[-\. ]?|\([1-9]\d{1,2}\)[-\. ]?)(\d{6,9}|\d{2,3}[-\. ]\d{4,6}))"
        us_numbers = re.findall(us_phone_pattern, response.text)

        phone_numbers = phone_numbers + us_numbers

        good_numbers = []
        if isinstance(phone_numbers, list):
            phone_numbers = set(phone_numbers)

            for number in phone_numbers:
                if '.' not in number and ',' not in number and len(number) >= 12:
                    good_numbers.append(number)
        print('good> ',good_numbers)
        yield {'url_collected': response.url,
               'logo_url': logo_url,
               'phone_numbers': good_numbers}