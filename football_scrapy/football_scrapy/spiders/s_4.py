import scrapy
from scrapy.shell import inspect_response

class Team_standings(scrapy.Item):
    position        = scrapy.Field()
    club        = scrapy.Field()
    games        = scrapy.Field()
    goals       = scrapy.Field()
    points        = scrapy.Field()
    season        = scrapy.Field()

class TeamStandingsSpider(scrapy.Spider):
    name = 'team_standings'
    allowed_domains = ['https://www.transfermarkt.pl/']

    years = range(2015,2022,1)

    #list of links with years
    start_urls = ['https://www.transfermarkt.pl/premier-league/startseite/wettbewerb/GB1/plus/?saison_id={}'.format(object) for object in years]

    def parse(self, response):

        #This part scrapes the other table, which contains data on team standings in a given season
        season = response.xpath('//*[@id="wettbewerbsstartseite"]/div[1]/div[2]/h2/text()').get().strip()[-5:]

        ts = Team_standings()

        if season != '21/22':

            t_rows = response.xpath('//div[@id="yw3"]/table/tbody/tr')
        
        else:
            t_rows = response.xpath('//div[@id="yw4"]/table/tbody/tr')

        for row in t_rows:
        
            ts['position'] = row.xpath('td[1]/text()').get()

            ts['club'] = row.xpath('td[2]/a/@title').get()

            ts['games'] = row.xpath('td[4]/text()').get()

            ts['goals'] = row.xpath('td[5]/text()').get()

            ts['points'] = row.xpath('td[6]/text()').get()

            ts['season'] = season

            yield ts
        

        