# Scraping transfermakt with Beautiful Soup, Selenium and Scrapy

The goal of this project is to scrape data about football teams and players in Premier League.

Set the limit_pages_100 parameter to True in order to limit the number of pages to scrape to a 100.




## Beautiful Soup

Run the soup.py file in the main folder WS2022 and scrape two data frames:
players and teams dataframe. You don't need to change anything in the code.


## Scrapy
If you clone the whole repository, the settings.py file will be adjusted propely and the script will execute without problems.

The most important part is the USER_AGENT variable, which must be set as in the settings.py file in the repository. Without this variable, transfermarkt does not allow to scrape their website.

The project folder is called 'football_scrapy'. You need to open that folder in order to run spiders.

Run the spiders in the following order:
s_1.py -> s_2.py -> s_3.py -> s_4.py in the spiders folder.

First spider (s_1.py) generates links for scraping the players. Please use the links.csv output name in order to create a csv file which will be used by the s_2 spider.

Second spider (s_2.py) does not require a specific name. You may use players.json name for the output.

Third spider (s_3.py) scrapes the main table with teams. If you want to merge this output with the output of the forth spider later in order to obtain complete table on teams, use the teams.csv output name and format.

Forth spider (s_4.py) scrapes tables with team standings. If you want to merge it with the third spider output, please use team_table.csv name for the output and format.

If you want to see the merged tables, please use the merged_tables.py file in the football_scrapy folder (the one inside the football_scrapy folder).

Use the following command to run a spider:
scrapy crawl {name of the spider} -O {name of the output file}.

## Selenium

Run the selenium.py and scrape two data frames:
players and teams dataframe. You don't have to change anything in the code, but you can. 
You can customize the time sleeps and select the seasons you want to scrape.
