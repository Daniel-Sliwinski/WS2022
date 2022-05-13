import scrapy

class Link(scrapy.Item):
    link = scrapy.Field()

class FootballSpider(scrapy.Spider):
    name = 'links'
    allowed_domains = ['https://www.transfermarkt.com/']
    #range of years to scrape
    years = range(2015,2022,1)

    #list of links with years
    start_urls = ['https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1/plus/?saison_id={}'.format(object) for object in years]

    def parse(self, response):

        xpath = '//*[@id="yw1"]/table/tbody/tr[*]/td[2]/a[1]/@href'
        selection = response.xpath(xpath)
        print(selection)

        for s in selection:
            l = Link()
            l['link'] = 'https://www.transfermarkt.com' + s.get()
            yield l