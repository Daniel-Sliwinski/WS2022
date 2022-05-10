# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup as bs
from scrapy.shell import inspect_response
import re

class Player(scrapy.Item):
    name        = scrapy.Field()
    position        = scrapy.Field()
    age        = scrapy.Field()
    nationality       = scrapy.Field()
    market_value        = scrapy.Field()
    season        = scrapy.Field()
    team        = scrapy.Field()

class LinksSpider(scrapy.Spider):
    name = 'players'
    allowed_domains = ['https://www.transfermarkt.pl/']
    try:
        with open("links.csv", "rt") as f:
            start_urls = [url.strip() for url in f.readlines()][1:]
    except:
        start_urls = []
    #print(start_urls)

    def parse(self, response):
        p = Player()
        
        rows = response.xpath('//*[@id="yw1"]/table/tbody/tr')

        tds = response.xpath('//*[@id="yw1"]/table/tbody/tr[1]/td')
        
        for td in tds:
            print(td.extract())
        
        #print(rows.get())

        print('')
        
        #print(all_tds)
        for row in rows:
            
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
            

            p['market_value'] = row.xpath('td[last()]/a/text()').get()

            season_header = response.xpath('//*[@id="main"]/div[6]/div[1]/div[1]/div[1]/h2/text()').get().strip()[-5:]
            pattern = '[0-9]+\/[0-9]'

            if re.search(pattern, season_header):
                p['season'] = season_header
            else:
                p['season'] = '21/22'
            print(p)
            yield p

        #inspect_response(response,self)



        #names = response.xpath('//*[@id="yw1"]/table/tbody/tr/td[2]/table/tbody/tr[1]/td[2]/div[1]/span/a/text()')

        #for nm in names:
            
        #    p['name'] = nm.xpath.get()

        #soup = bs(response.text, 'lxml')
        #print(soup)

        #print(soup.xpath('/html/body/div[4]/div[4]/div/div[1]/div[1]/div/div[1]/h1/span'))
        #name_xpath = '/html/body/div[4]/div[4]/div/div[1]/div[1]/div/div[1]/h1/span'
        #print(response.xpath(name_xpath).get())
        #position_xpath       = '//*[@id="yw1"]/table/tbody/tr[*]/td[2]/table/tbody/tr[2]/td'
        #print(start_urls)

        #p['name']= response.xpath(name_xpath).getall()
        #print(response.xpath(name_xpath).get())
        #p['position']       = response.xpath(position_xpath).getall()

        #yield p

