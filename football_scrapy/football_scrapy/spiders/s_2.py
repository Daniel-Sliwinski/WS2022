#This spider scrapes players from all teams.
#Set parameter of pages to scrape to true if you want to limit them to 100:
limit_pages_100 = True

# -*- coding: utf-8 -*-
import scrapy
import re

class Player(scrapy.Item):
    name        = scrapy.Field()
    position        = scrapy.Field()
    age        = scrapy.Field()
    nationality       = scrapy.Field()
    market_value        = scrapy.Field()
    season        = scrapy.Field()
    team        = scrapy.Field()
    current_club = scrapy.Field()


class LinksSpider(scrapy.Spider):

    name = 'players'
    allowed_domains = ['https://www.transfermarkt.com/']

    try:
        with open("links.csv", "rt") as f:
            start_urls = [url.strip() for url in f.readlines()][1:]
    except:
        start_urls = []

    if limit_pages_100:
        start_urls = start_urls[:100]
    else:
        pass

    def parse(self, response):

        p = Player()
        
        rows = response.xpath('//*[@id="yw1"]/table/tbody/tr')
        
        season_header = response.xpath('//*[@id="main"]/div[6]/div[1]/div[1]/div[1]/h2/text()').get().strip()[-5:]
        
        for row in rows:

            pattern = '[0-9]+\/[0-9]'

            if re.search(pattern, season_header):
                p['season'] = season_header
            else:
                p['season'] = '21/22'

            
            p['team'] = response.xpath('//div[@id="verein_head"]/div/div[1]/div[1]/div/div[1]/h1/span/text()').get()


            try:
                p['name'] = row.xpath("td[2]/following::span[@class='hide-for-small'][1]/a/text()").get()
            except:
                p['name'] = row.xpath('td[3]/text()').get()


            p['position'] = row.xpath('td[1]/@title').get()


            p['age'] = row.xpath("td[@class='zentriert'][1]/text()").get()


            try:
                p['nationality'] = row.xpath("td[@class='zentriert'][1]/following-sibling::td[1]/img/@title").get()
            except:
                p['nationality'] = row.xpath('td[4]/img/@title').get()
            

            if re.search(pattern, season_header):
                p['current_club'] = row.xpath('td[5]/a/@title').get()
            else:
                p['current_club'] = response.xpath('//div[@id="verein_head"]/div/div[1]/div[1]/div/div[1]/h1/span/text()').get()


            p['market_value'] = row.xpath('td[last()]/a/text()').get()

            yield p

