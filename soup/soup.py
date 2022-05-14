#This code scrapes players and teams at the same time.
#Set parameter of pages to scrape to true if you want to limit them to 100:
limit_pages_100 = True

import requests
from bs4 import BeautifulSoup as BS
import pandas as pd
import re

#personal data for getting access to the site
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"}

#range of years to scrape
years = range(2015,2022,1)

#list of links with years
url_list = ['https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1/plus/?saison_id={}'.format(object) for object in years]

#the final list of links with teams to scrape
links = []

#open each url and scrape links of all teams
for url in url_list:
    html = requests.get(url, headers=headers)
    bs = BS(html.content, 'html.parser')

    rows = bs.find('h2', string=re.compile('Clubs - Premier League.*')).findNext('tbody').find_all('tr')

    temp_tags = [row.find_all('td')[1].a for row in rows]

    
    link_temp_list = ['https://www.transfermarkt.com' + tag['href'] for tag in temp_tags]
    
    links.extend(link_temp_list)

#this prepares a data frame for soccer players
d = pd.DataFrame({'name':[], 'position':[], 'age':[], 'nationality':[], 'market_value':[], 'season':[], 'team':[], 'current_team':[]})

if limit_pages_100:
    links = links[:100]
else:
    pass

for link in links:
    html = requests.get(link, headers=headers)
    bs = BS(html.content, 'html.parser')

    rows = bs.find_all('tr', {'class': ['odd', 'even']})

    for row in rows:
        all_tds = row.find_all('td', recursive = False)

        try:
            name = all_tds[1].find('div', {'class':'di nowrap'}).text
        except:
            name = ''
        
        try:
            position = all_tds[1].find_all('tr')[-1].text
        except:
            position = ''
        
        season = bs.find('div', {'class':'subkategorie-header'}).h2.text.strip()[-5:]
        pattern = '[0-9]+\/[0-9]'

        if re.search(pattern, season):
            pass
        else:
            season = '21/22'

        if season != '21/22':
            age = all_tds[2].text
        else:
            age = all_tds[2].text
        
        if season != '21/22':
            nationality = all_tds[3].find('img')['title']
        else:
            nationality = all_tds[4].find('img')['title']
        
        try:
            market_value = all_tds[5].find('a').text
        except:
            market_value = ''
        
        try:
            team = bs.find('div', {'id':'verein_head'}).h1.text.strip()
        except:
            team = ''

        if season != '21/22':
            try:
                current_team = all_tds[-2].a['title']
            except:
                current_team = ''
        else:
            current_team = team

        player = {'name':name, 'position':position, 'age':age, 'nationality':nationality, 'market_value':market_value, 'season':season, 'team':team, 'current_team':current_team}

        d = d.append(player, ignore_index = True)

#this prepares a data frame for teams
teams = pd.DataFrame({'season':[], 'team':[], 'players':[], 'avg_age':[], 'foreigners':[], 'avg_market_value':[], 'total_market_value':[]})

#this prepares the other data frame for team standings
team_standings = pd.DataFrame({'position':[], 'team':[], 'games':[], 'goals':[], 'points':[], 'season':[]})


for link in url_list:
    html = requests.get(link, headers=headers)
    bs = BS(html.content, 'html.parser')

    rows = bs.find('div', {'id':'yw1'}).table.tbody.find_all('tr', recursive = False)

    for row in rows:
        all_tds = row.find_all('td', recursive= False)


        try:
            season = all_tds[0].a['href'].strip()[-2:] + '/' + str(int(all_tds[0].a['href'].strip()[-2:]) + 1)
        except:
            season = ''

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

        try:
            foreigners = all_tds[4].text
        except:
            foreigners = ''

        try:
            avg_market_value = all_tds[5].text
        except:
            avg_market_value = ''

        try:
            total_market_value = all_tds[6].a.text
        except:
            total_market_value = ''

        team = {'season':season, 'team':team, 'players':players, 'avg_age':avg_age, 'foreigners':foreigners, 'avg_market_value':avg_market_value, 'total_market_value':total_market_value}
        
        teams = teams.append(team, ignore_index = True)

    #This part scrapes the table with team standings
    if season != '21/22':
        t_rows = bs.find('div', {'id':'yw4'}).table.tbody.find_all('tr', recursive = False)
    else:
        t_rows = bs.find('div', {'id':'yw5'}).table.tbody.find_all('tr', recursive = False)
    
    for row in t_rows:
        all_tds = row.find_all('td', recursive= False)

        try:
            position = all_tds[0].text
        except:
            position = ''

        try:
            team = all_tds[1].a['title']
        except:
            team = ''
        try:
            games = all_tds[3].text
        except:
            games = ''

        try:
            goals = all_tds[4].text
        except:
            goals = ''

        try:
            points = all_tds[5].text
        except:
            points = ''
        team_st = {'season':season, 'team':team, 'position':position, 'games':games, 'goals':goals, 'points':points}
        
        team_standings = team_standings.append(team_st, ignore_index = True)
        
        
full_team_df = pd.merge(teams, team_standings, left_on = ['season','team'], right_on=['season','team'], copy = False)
print(full_team_df)

print(d)

d.to_csv('players.csv')