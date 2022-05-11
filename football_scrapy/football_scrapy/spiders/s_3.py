#This spider scrapes information about Premier League teams.
import scrapy
from scrapy.shell import inspect_response

class Team(scrapy.Item):
    season        = scrapy.Field()
    club        = scrapy.Field()
    players        = scrapy.Field()
    avg_age       = scrapy.Field()
    foreigners        = scrapy.Field()
    avg_market_value        = scrapy.Field()
    total_market_value        = scrapy.Field()

class Team_standings(scrapy.Item):
    position        = scrapy.Field()
    club        = scrapy.Field()
    games        = scrapy.Field()
    goals       = scrapy.Field()
    points        = scrapy.Field()
    season        = scrapy.Field()



class TeamSpider(scrapy.Spider):
    name = 'teams'
    allowed_domains = ['https://www.transfermarkt.pl/']


    years = range(2015,2022,1)

    #list of links with years
    start_urls = ['https://www.transfermarkt.pl/premier-league/startseite/wettbewerb/GB1/plus/?saison_id={}'.format(object) for object in years]

    def parse(self, response):
        t = Team()

        rows = response.xpath('//div[@id="yw1"]/table/tbody/tr')

        for row in rows:
            print(row.extract())

            t['season'] = response.xpath('//*[@id="wettbewerbsstartseite"]/div[1]/div[2]/h2/text()').get().strip()[-5:]

            t['club'] = row.xpath("td[1]/a/@title").get()

            t['players'] = row.xpath("td[3]/a/text()").get()

            t['avg_age'] = row.xpath("td[4]/text()").get()

            t['foreigners'] = row.xpath("td[5]/text()").get()

            t['avg_market_value'] = row.xpath("td[6]/text()").get()

            t['total_market_value'] = row.xpath("td[7]/a/text()").get()

            yield t


        #This part scrapes the other table, which contains data on team standings in a given season

        t_rows = response.xpath('//div[@id="yw3"]/table/tbody/tr')

        ts = Team_standings()

        for row in t_rows:
            ts['position'] = row.xpath('td[1]/text()').get()

            yield ts

        #inspect_response(response,self)

