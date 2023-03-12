import logging
import os

import click
from scrapy.crawler import CrawlerProcess

from websites_scraper.spiders.google_contact_search import GoogleContactSearchSpider
from websites_scraper.spiders.websites_data_collection import WebsitesDataCollectionSpider

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


@click.command("scrape-url")
@click.option("--url", type=click.STRING, help="Website url to scrape data", default=None)
@click.option("--output-path", type=click.STRING, help="Your local path to save files", default="")
def main(url: str, output_path: str):
    """
    Main program execution.
    https://www.randomlists.com/urls

    bash to output docker files
    docker run -it -v /path/to/local/folder:/data scrapy-image scrapy crawl spider_name -o /data/output.json


    :param output_path:
    :type url: url to search
    :return: .json file
    """
    logging.debug(str(f"Initializing data collector"))
    logging.info(str(f"Searching url: {url}"))
    logging.info(str(f"Output path: {output_path}"))

    try:
        os.remove('collected_website_data.json')
    except FileNotFoundError:
        pass

    process = CrawlerProcess(settings={'BOT_NAME': 'websites_scraper',
                                       'ROBOTSTXT_OBEY': False,
                                       'CONCURRENT_ITEMS': 32,
                                       'CONCURRENT_REQUESTS_PER_DOMAIN': 16,
                                       'CONCURRENT_REQUESTS_PER_IP': 16,
                                       'DOWNLOAD_TIMEOUT': 6,
                                       'FEED_EXPORT_ENCODING': 'utf-8',
                                       'NEWSPIDER_MODULE': 'websites_scraper.spiders',
                                       'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',
                                       'RETRY_ENABLED': False,
                                       'RETRY_HTTP_CODES': [500, 502, 503, 504, 522, 524, 408],
                                       'RETRY_TIMES': 5,
                                       'FEED_FORMAT': 'json',
                                       'FEED_URI': str(f"{output_path}/collected_website_data.json"),
                                       'SPIDER_MODULES': ['websites_scraper.spiders'],
                                       'TWISTED_REACTOR': 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'}

                             )

    process.crawl(WebsitesDataCollectionSpider, url)
    process.start()


@click.command("create-parameters")
@click.option("--search-string", type=click.STRING, help="", default='contact us')
def parameter_creation(search_string: str):
    """
    Creates parameters to use in tests.

    bash to output docker files
    docker run -it -v /path/to/local/folder:/data scrapy-image scrapy crawl spider_name -o /data/output.json

    :param search_string: string to search on Google
    :return: .json file
    """
    logging.debug(str(f"Initializing data collector"))
    logging.info(str(f"Searching parameters on google: {search_string}"))

    try:
        os.remove('output_parameters.json')
    except FileNotFoundError:
        pass

    process = CrawlerProcess(settings={'BOT_NAME': 'parameter_creation',
                                       'ROBOTSTXT_OBEY': True,
                                       'CONCURRENT_ITEMS': 2,
                                       'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
                                       'CONCURRENT_REQUESTS_PER_IP': 2,
                                       'DOWNLOAD_TIMEOUT': 5,
                                       'FEED_EXPORT_ENCODING': 'utf-8',
                                       'NEWSPIDER_MODULE': 'websites_scraper.spiders',
                                       'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',
                                       'RETRY_ENABLED': True,
                                       'RETRY_HTTP_CODES': [500, 502, 503, 504, 522, 524, 408],
                                       'RETRY_TIMES': 5,
                                       'FEED_FORMAT': 'json',
                                       'FEED_URI': 'output_parameters.json',
                                       'SPIDER_MODULES': ['websites_scraper.spiders'],
                                       'TWISTED_REACTOR': 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'}

                             )

    process.crawl(GoogleContactSearchSpider, search_string)
    process.start()


if __name__ == '__main__':
    main()
