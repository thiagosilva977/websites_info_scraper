import scrapy


class WebsitesDataCollectionSpider(scrapy.Spider):
    name = "websites_data_collection"
    allowed_domains = ["www.illion.com.au"]
    start_urls = ["http://www.illion.com.au/"]

    def parse(self, response):
        pass
