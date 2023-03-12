import ast
import logging
import re

import scrapy

from websites_scraper.testing_parameters import random_websites_parameters

# Logging basic config
logging.basicConfig(format="%(asctime)s %(message)s", datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


class WebsitesDataCollectionSpider(scrapy.Spider):
    def __init__(self, input_url=None, **kwargs):
        super().__init__(**kwargs)
        if input_url is None:
            input_url = random_websites_parameters
        self._input_url = input_url

    name = "websites_data_collection"

    def start_requests(self):
        """
        Function responsible for doing requests

        :return: scrapy request targeting to parse function
        """
        if isinstance(self._input_url, list):
            for url_to_scrape in self._input_url:
                yield scrapy.Request(url=url_to_scrape, callback=self.parse)

        elif self._input_url is None:
            logging.warning('Input URL received is None. Changing to testing URLs ...')
            yield scrapy.Request(url=random_websites_parameters, callback=self.parse)

        else:
            if '[' in self._input_url and ']' in self._input_url:
                my_list = ast.literal_eval(self._input_url)
                split_urls = my_list
                for url_to_scrape in split_urls:
                    yield scrapy.Request(url=url_to_scrape, callback=self.parse)

            elif ',' in self._input_url:
                split_urls = self._input_url.split(',')
                for url_to_scrape in split_urls:
                    yield scrapy.Request(url=url_to_scrape, callback=self.parse)

            else:

                yield scrapy.Request(url=self._input_url, callback=self.parse)

    def parse(self, response, **kwargs):
        """
        Function responsible for parsing scrapy.Request content.

        :param response: scrapy response (like requests library)
        :param kwargs: additional arguments
        :return: collected data dict
        """
        # Find website url
        parsed_website_url = response.url

        # Find icon url
        base_icon_url_href = response.css('link[rel="shortcut icon"]::attr(href)').extract_first()
        parsed_logo_icon_url = None
        parsed_website_domain = None
        domain_regex = re.compile(r'^(https?://(?:www\.)?\w+\.\w{2,3}(?:\.\w{2})?)')
        match_domain = domain_regex.search(parsed_website_url)
        if match_domain:
            parsed_website_domain = match_domain.group(1)
            if base_icon_url_href is not None and "http" not in base_icon_url_href:
                parsed_logo_icon_url = str(f"{match_domain.group(1)}{base_icon_url_href}")
            elif base_icon_url_href is not None:
                parsed_logo_icon_url = str(f"{base_icon_url_href}")

        # Find some img src that contains "logo"
        parsed_logo_url = response.css('img[src*=logo]::attr(src)').get()

        if parsed_logo_url is not None and 'http' not in parsed_logo_url:
            parsed_logo_url = str(f"{parsed_website_domain}{parsed_logo_url}")

        # Find phone numbers
        phone_numbers_list = []

        brazilian_phone_pattern = r"(?:\+?\d{1,3}[- ]?)?\(?\d{2,3}\)?[- ]?\d{4,5}[- ]?\d{4}"
        brazilian_numbers = re.findall(brazilian_phone_pattern, response.text)

        phone_numbers_list = phone_numbers_list + brazilian_numbers

        us_phone_pattern = r"(?:^|\s)(((?:\+|0{2})(?:49|43|33)[-\. ]?|0)([1-9]\d{1,2}[-\. ]?|\([1-9]\d{1,2}\)[-\. " \
                           r"]?)(\d{6,9}|\d{2,3}[-\. ]\d{4,6}))"
        us_numbers = re.findall(us_phone_pattern, response.text)

        phone_numbers_list = phone_numbers_list + us_numbers

        parsed_phone_numbers_list = []
        if isinstance(phone_numbers_list, list):
            # Remove duplicates
            phone_numbers_list = set(phone_numbers_list)
            # Filter results
            for number in phone_numbers_list:
                if '.' not in number and ',' not in number and len(number) >= 12:
                    parsed_phone_numbers_list.append(number)
        # Return collected data to scrapy
        yield {'url_collected': parsed_website_url,
               'icon_url': parsed_logo_icon_url,
               'logo_url': parsed_logo_url,
               'phone_numbers': parsed_phone_numbers_list}
