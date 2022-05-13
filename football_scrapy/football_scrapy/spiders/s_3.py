#This spider scrapes information about Premier League teams.
import scrapy
from scrapy.shell import inspect_response

class Team(scrapy.Item):
    season        = scrapy.Field()
    team        = scrapy.Field()
    players        = scrapy.Field()
    avg_age       = scrapy.Field()
    foreigners        = scrapy.Field()
    avg_market_value        = scrapy.Field()
    total_market_value        = scrapy.Field()

class TeamSpider(scrapy.Spider):
    name = 'teams'
    allowed_domains = ['https://www.transfermarkt.com/']


    years = range(2015,2022,1)

    #list of links with years
    start_urls = ['https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1/plus/?saison_id={}'.format(object) for object in years]

    def parse(self, response):
        t = Team()

        rows = response.xpath('//div[@id="yw1"]/table/tbody/tr')

        for row in rows:

            t['season'] = response.xpath('//*[@id="wettbewerbsstartseite"]/div[1]/div[2]/h2/text()').get().strip()[-5:]

            t['team'] = row.xpath("td[1]/a/@title").get()

            t['players'] = row.xpath("td[3]/a/text()").get()

            t['avg_age'] = row.xpath("td[4]/text()").get()

            t['foreigners'] = row.xpath("td[5]/text()").get()

            t['avg_market_value'] = row.xpath("td[6]/text()").get()

            t['total_market_value'] = row.xpath("td[7]/a/text()").get()

            yield t


