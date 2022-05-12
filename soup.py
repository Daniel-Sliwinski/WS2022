import requests
from bs4 import BeautifulSoup as BS
import pandas as pd
import re

#personal data for getting access to the site
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"}

#range of years to scrape
years = range(2015,2022,1)

#list of links with years
url_list = ['https://www.transfermarkt.pl/premier-league/startseite/wettbewerb/GB1/plus/?saison_id={}'.format(object) for object in years]

#the final list of links with teams to scrape
links = []

#open each url and scrape links of all teams
for url in url_list:
    html = requests.get(url, headers=headers)
    bs = BS(html.content, 'html.parser')

    rows = bs.find('h2', string=re.compile('Kluby Premier League.*')).findNext('tbody').find_all('tr')

    temp_tags = [row.find_all('td')[1].a for row in rows]

    
    link_temp_list = ['https://www.transfermarkt.pl' + tag['href'] for tag in temp_tags]
    
    links.extend(link_temp_list)



print(links)

#this prepares a data frame for soccer players
d = pd.DataFrame({'name':[], 'position':[], 'age':[], 'nationality':[], 'market_value':[], 'season':[], 'team':[]})


#for link in links[:2]:
#    html = requests.get(link, headers=headers)
#    bs = BS(html.content, 'html.parser')
#
#
#    rows = bs.find_all('tr', {'class': ['odd', 'even']})
#
#    for row in rows:
#        all_tds = row.find_all('td', recursive = False)
#        #print('this is next row')
#        try:
#            name = all_tds[1].find('div', {'class':'di nowrap'}).text
#        except:
#            name = ''
#        print(name)
#        
#        try:
#            position = all_tds[1].find_all('tr')[-1].text
#        except:
#            position = ''
#        
#        try:
#            age = all_tds[2].text
#        except:
#            age = ''
#        
#        try:
#            nationality = all_tds[3].find('img')['title']
#        except:
#            nationality = ''
#        
#        try:
#            market_value = all_tds[5].find('a').text
#        except:
#            market_value = ''
#        
#        try:
#            season = bs.find('div', {'class':'subkategorie-header'}).h2.text.strip()[-5:]
#        except:
#            season = ''
#        
#        try:
#            team = bs.find('div', {'id':'verein_head'}).h1.text.strip()
#        except:
#            team = ''
#        
#        player = {'name':name, 'position':position, 'age':age, 'nationality':nationality, 'market_value':market_value, 'season':season, 'team':team}
#
#        d = d.append(player, ignore_index = True)
#    #print(d)


#this prepares a data frame for teams
teams = pd.DataFrame({'season':[], 'team':[], 'players':[], 'avg_age':[], 'foreigners':[], 'avg_market_value':[], 'total_market_value':[]})

for link in url_list[:2]:
    html = requests.get(link, headers=headers)
    bs = BS(html.content, 'html.parser')

    rows = bs.find('div', {'id':'yw1'}).table.tbody.find_all('tr', recursive = False)

    for row in rows:
        all_tds = row.find_all('td', recursive= False)
        print(all_tds)
        print('')

        

        try:
            season = all_tds[0].a['href'].strip()[-2:] + '/' + str(int(all_tds[0].a['href'].strip()[-2:]) + 1)
        except:
            season = ''
        #
        try:
            team = all_tds[0].a['title']
        except:
            team = ''
        
        try:
            players = all_tds[2].a.text
        except:
            players = ''
        
        try:
            avg_age = all_tds[3].text
        except:
            avg_age = ''
        #
        try:
            foreigners = all_tds[4].text
        except:
            foreigners = ''
        #
        try:
            avg_market_value = all_tds[5].text
        except:
            avg_market_value = ''
        #
        try:
            total_market_value = all_tds[6].a.text
        except:
            total_market_value = ''

        team = {'season':season, 'team':team, 'players':players, 'avg_age':avg_age, 'foreigners':foreigners, 'avg_market_value':avg_market_value, 'total_market_value':total_market_value}
        
        teams = teams.append(team, ignore_index = True)
    #print(teams)
#d.to_csv('players.csv')