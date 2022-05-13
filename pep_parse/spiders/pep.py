import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        all_documents = response.css('a[href^="pep"]')
        for document_link in all_documents:
            yield response.follow(document_link, callback=self.parse_pep)

    def parse_pep(self, response):
        response_title = ' '.join(
            response.css('h1.page-title *::text').getall())
        split_title = response_title.split()
        data = {
            'number': int(split_title[1]),
            'name': response_title,
            'status': response.css('dt:contains("Status") + dd::text').get(),
        }
        yield PepParseItem(data)
