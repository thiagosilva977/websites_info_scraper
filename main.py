import logging
import os

import click

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


@click.command("scrape-url")
@click.option("--url", type=click.STRING, help="", default='https://www.illion.com.au/contact-us/')
def main(url: str):
    """
    Main program execution.
    https://www.randomlists.com/urls

    bash to output docker files
    docker run -it -v /path/to/local/folder:/data scrapy-image scrapy crawl spider_name -o /data/output.json


    :type url: object
    :return:
    """
    logging.debug(str(f"Initializing data collector"))
    logging.info(str(f"Searching url {url}"))

    try:
        os.remove('output.json')
    except FileNotFoundError:
        pass

    from scrapy.crawler import CrawlerProcess
    from websites_scraper.spiders.websites_data_collection import WebsitesDataCollectionSpider

    process = CrawlerProcess(settings={'BOT_NAME': 'websites_scraper',
                                       'ROBOTSTXT_OBEY': False,
                                       'CONCURRENT_ITEMS': 32,
                                       'CONCURRENT_REQUESTS_PER_DOMAIN': 16,
                                       'CONCURRENT_REQUESTS_PER_IP': 16,
                                       'DOWNLOAD_TIMEOUT': 5,
                                       'FEED_EXPORT_ENCODING': 'utf-8',
                                       'NEWSPIDER_MODULE': 'websites_scraper.spiders',
                                       'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',
                                       'RETRY_ENABLED': False,
                                       'RETRY_HTTP_CODES': [500, 502, 503, 504, 522, 524, 408],
                                       'RETRY_TIMES': 5,
                                       'FEED_FORMAT': 'json',
                                       'FEED_URI': 'output.json',
                                       'SPIDER_MODULES': ['websites_scraper.spiders'],
                                       'TWISTED_REACTOR': 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'}

                             )

    process.crawl(WebsitesDataCollectionSpider, url)
    process.start()


@click.command("create-parameters")
@click.option("--search-string", type=click.STRING, help="", default='contact us')
def parameter_creation(search_string: str):
    """
    Main program execution.
    https://www.randomlists.com/urls

    bash to output docker files
    docker run -it -v /path/to/local/folder:/data scrapy-image scrapy crawl spider_name -o /data/output.json


    :param search_string:
    :return:
    """
    logging.debug(str(f"Initializing data collector"))
    logging.info(str(f"Searching parameters on google: {search_string}"))

    try:
        os.remove('output_string.json')
    except FileNotFoundError:
        pass

    from scrapy.crawler import CrawlerProcess
    from websites_scraper.spiders.google_contact_search import GoogleContactSearchSpider

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
