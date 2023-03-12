import re
import scrapy
from googlesearch import search


class GoogleContactSearchSpider(scrapy.Spider):
    def __init__(self, search_input=None, **kwargs):
        super().__init__(**kwargs)
        if search_input is None:
            search_input = 'contact-us'
        self._input_string = search_input
    name = "google_contact"
    start_urls = ["https://www.google.com/"]

    def parse(self, response, **kwargs):
        search_query = self._input_string
        for url in search(search_query, num_results=100):
            yield scrapy.Request(url, callback=self.parse_website)

    @staticmethod
    def parse_website(response):
        # Filter URLs that don't contain "contact" or "about" in the path or domain
        if not re.search(r"(contact|about)", response.url, re.IGNORECASE):
            return

        # Check if the page has a "contact" or "about" link
        has_contact_link = False
        for link in response.xpath("//a"):
            href = link.xpath("./@href").get()
            if href and re.search(r"(contact|about)", href, re.IGNORECASE):
                has_contact_link = True
                break

        # If the page has a "contact" or "about" link, yield the URL
        if has_contact_link:
            yield {
                "url": response.url
            }
