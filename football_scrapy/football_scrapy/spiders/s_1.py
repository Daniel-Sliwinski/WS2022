import scrapy

class Link(scrapy.Item):
    link = scrapy.Field()

class MusiciansSpider(scrapy.Spider):
    name = 'link_lists'
    allowed_domains = ['https://en.wikipedia.org/']
    start_urls = ['https://en.wikipedia.org/wiki/Lists_of_musicians']

    def parse(self, response):

        xpath = '//*[@id="mw-content-text"]/div[1]/div[4]/ul/li/a/@href'
        selection = response.xpath(xpath)
        print(selection)

        for s in selection:
            l = Link()
            l['link'] = 'https://en.wikipedia.org' + s.get()
            yield l