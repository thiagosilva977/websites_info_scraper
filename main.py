import click
import logging

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


@click.command("scrape-url")
@click.option("--url", type=click.STRING, help="", default='https://www.illion.com.au/contact-us/')
@click.option("--is-running-local/--is-not-running-local", default=False)
def main(url: str,
         is_running_local: bool,
         ):
    """
    Main program execution.
    https://www.randomlists.com/urls

    :type url: object
    :param is_running_local: If program is running on local machine.
    :return:
    """
    logging.debug(str(f"Initializing data collector"))
    logging.info(str(f"Searching url {url}"))

    from scrapy.crawler import CrawlerProcess
    from websites_scraper.spiders.websites_data_collection import WebsitesDataCollectionSpider

    process = CrawlerProcess(settings={'BOT_NAME': 'websites_scraper',
                                       'ROBOTSTXT_OBEY': False,
                                       'CONCURRENT_ITEMS': 32,
                                       'CONCURRENT_REQUESTS_PER_DOMAIN': 16,
                                       'CONCURRENT_REQUESTS_PER_IP': 16,
                                       'DOWNLOAD_TIMEOUT': 2,
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

    # process = CrawlerProcess()

    urls = ['https://docs.scrapy.org/en/latest/intro/tutorial.html#our-first-spider',
            'https://stackoverflow.com/questions/53733190/is-scrapy-compatible-with-multiprocessing',
            'https://www.illion.com.au/contact-us/',
            'https://www.oakley.com', 'https://www.latimes.com', 'https://www.dmoz.org',
            'https://www.msu.edu', 'https://www.yahoo.com', 'https://www.auda.org.au']

    #urls = ['https://support.google.com/business/answer/7690269?hl=en']
    #urls = ['https://www.stylemanual.gov.au/grammar-punctuation-and-conventions/numbers-and-measurements/telephone-numbers']
    #urls = ['https://www.bb.com.br/site/pra-voce/atendimento/']

    process.crawl(WebsitesDataCollectionSpider, urls)
    process.start()


if __name__ == '__main__':
    main()
