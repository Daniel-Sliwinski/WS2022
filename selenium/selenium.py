from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd

#boolean parameter limiting the number of pages
pages_limit = True

#Set the local path to driver.exe
path = "C:\\Users\\leski\\OneDrive\\Pulpit\\DS\\WebScrapping\\chromedriver.exe"

options = webdriver.chrome.options.Options()
options.headless = False
driver = webdriver.Chrome(options = options, executable_path=path) # 



# Function to scrape clubs tables 
def scrape_clubs(start_year, end_year):
    
    #creating empty lists for both tables
    season = []
    club = []
    players = []
    avg_age =[]
    foreigners = []
    avg_market_value = []
    total_market_value = []

    t_club = []
    t_position = [] 
    t_goals = []
    t_games = []
    t_points = []
    t_season = []

    #loop for iterating through the seasons
    for year in range(start_year,end_year+1,1):
        url = 'https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1/plus/?saison_id='+str(year)
        driver.get(url)
        time.sleep(5)
        
        #those lines below count the total number of table's rows and columns 
        #It is needed for further loop   
        rows = 1+len(driver.find_elements_by_xpath(
            '//*[@id="yw1"]/table//tbody//tr'))

        cols = 1+len(driver.find_elements_by_xpath(
            '//*[@id="yw1"]/table//th'))

        for r in range(1, rows):
            for c in range(2,cols):
            # obtaining the text from each column of the table
                if (c in range(2,4)):
                    value = driver.find_element(by=By.XPATH, value =
                        '//*[@id="yw1"]/table//tbody//tr['+str(r)+']/td['+str(c)+']/a').text
                    if (c == 2):
                        club.append(value)
                        
                    if (c == 3):
                        players.append(value)
                else:
                    value = driver.find_element(by=By.XPATH, value =
                        '//*[@id="yw1"]/table//tbody//tr['+str(r)+']/td['+str(c)+']').text
                    if(c == 4):
                        avg_age.append(value)
                        
                    if(c == 5):
                        foreigners.append(value)
                        
                    if(c == 6):
                        avg_market_value.append(value)
                    if(c == 7):
                        total_market_value.append(value)

            #appending season_id for further merging tables     
            season.append(str(year)+'/'+str(year+1))
        
        #its necessery to include if condition for season == 2021, because of the diffrences in pages layout in current season and previous ones 
        if (year == 2021): 
            t_rows = 1+len(driver.find_elements_by_xpath(
                '//*[@id="yw5"]/table//tbody//tr'))
            t_cols = 2+len(driver.find_elements_by_xpath(
                '//*[@id="yw5"]/table//th'))
        else:
            t_rows = 1+len(driver.find_elements_by_xpath(
                '//*[@id="yw4"]/table//tbody//tr'))
            t_cols = 2+len(driver.find_elements_by_xpath(
                '//*[@id="yw4"]/table//th'))
        # obtaining the text from each column of the second table
        for tr in range(1, t_rows):
            for tc in range(1,t_cols):
                if (year == 2021):
                    t_value = driver.find_element(by=By.XPATH, value =
                            '//*[@id="yw5"]/table//tbody//tr['+str(tr)+']/td['+str(tc)+']').text
                else:
                    t_value = driver.find_element(by=By.XPATH, value =
                            '//*[@id="yw4"]/table//tbody//tr['+str(tr)+']/td['+str(tc)+']').text
                if (tc == 1):
                    t_position.append(t_value)
                if (tc == 3):
                    if(year == 2021):
                        t_value = driver.find_element(by=By.XPATH, value =
                                '//*[@id="yw5"]/table//tbody//tr['+str(tr)+']/td['+str(tc)+']/a').get_attribute('title')
                    else:
                        t_value = driver.find_element(by=By.XPATH, value =
                                '//*[@id="yw4"]/table//tbody//tr['+str(tr)+']/td['+str(tc)+']/a').get_attribute('title')
                    t_club.append(t_value)
                if (tc == 4):
                    t_games.append(t_value)
                if(tc == 5):
                    t_goals.append(t_value)
                if(tc == 6):
                    t_points.append(t_value)
            t_season.append(str(year)+'/'+str(year+1))    
            

    #creating and merging final dataframes         
    zipped_clubs = zip(season, club, players, avg_age, foreigners, avg_market_value, total_market_value)
    zipped_table = zip(t_season, t_position, t_club, t_games, t_goals, t_points)
    df_clubs = pd.DataFrame(zipped_clubs, columns= ['season', 'club', 'players', 'avg_age', 'foreigners', 'avg_market_value', 'total_market_value'])
    df_table = pd.DataFrame(zipped_table, columns = ['t_season', 't_position', 't_club', 't_games', 't_goals', 't_points'])
    full_table = pd.merge(df_table, df_clubs, left_on = ['t_season','t_club'], right_on=['season','club'], copy = False)
    print(df_clubs, df_table, full_table)
    
        
    return(full_table)

#player scraping function
#parameter 'limit_pages' added 
def scrape_players(start_year,end_year, limit_pages):
    limit = limit_pages
    x = 0 
    p_season = []
    team = []
    player = []
    p_position = []
    birth = []
    nationality = []
    current_club = []
    market_value = []

    #this part is crucial to dealing with the acceptance of cookies, it has to be done only once 
    url_start = 'https://www.transfermarkt.com'
    driver.get(url_start)
    driver.switch_to.frame('sp_message_iframe_575843')
    button_path = '/html/body/div/div[2]/div[3]/div[2]/button'
    time.sleep(5)

    button = driver.find_element(By.XPATH, button_path)
    button.click()

    time.sleep(3)

    # actual loop for scraping players through the seasons 
    for year in range(start_year,end_year+1,1):
        url = 'https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1/plus/?saison_id='+str(year)
        driver.get(url)
        rows = 1+len(driver.find_elements_by_xpath(
            '//*[@id="yw1"]/table//tbody//tr'))
        for r in range(1, rows):
            if(x<limit): #pages_limit condition 
                try:
                    x +=1
                    print(x)
                    value = driver.find_element(by=By.XPATH, value =
                        '//*[@id="yw1"]/table//tbody//tr['+str(r)+']/td[2]/a')
                    value.click()
                    time.sleep(1)
                    t_rows = 1+ len(driver.find_elements_by_xpath(
                        '//*[@id="yw1"]/table//tbody/tr[contains(@class, "odd") or contains(@class, "even")]'))
                    t_cols = 1+len(driver.find_elements_by_xpath(
                        '//*[@id="yw1"]/table//th'))
                    team_value = driver.find_element(by=By.XPATH, value=
                                    '//*[@id="verein_head"]/div/div[1]/div[1]/div/div[1]/h1/span').text
                    
                    # obtaining the text from each column of the players tables 
                    for tr in range(1, t_rows):
                        team.append(team_value)
                        p_season.append(str(year)+'/'+str(year+1)) 
                        for tc in range(2,t_cols):
                            t_value = driver.find_element(by=By.XPATH, value =
                                            '//*[@id="yw1"]/table//tbody//tr['+str(tr)+']/td['+str(tc)+']').text
                            if(tc == 2):
                                t_value_z = driver.find_element(by=By.XPATH, value =
                                            '//*[@id="yw1"]/table//tbody//tr['+str(tr)+']/td[2]/table/tbody/tr[1]/td[2]//span[@class="show-for-small"]/a').get_attribute('title')
                                player.append(t_value_z)
                                
                                t_value_y = driver.find_element(by=By.XPATH, value =
                                            '//*[@id="yw1"]/table//tbody//tr['+str(tr)+']/td[2]/table/tbody/tr[2]/td').text
                                p_position.append(t_value_y)
                            if(tc == 3):
                                if(year == 2021):
                                    t_value = driver.find_element(by=By.XPATH, value =
                                            '//*[@id="yw1"]/table//tbody//tr['+str(tr)+']/td['+str(tc+1)+']').text
                                    birth.append(t_value)
                                else:
                                    birth.append(t_value)
                                
                            if(tc == 4):
                                if(year == 2021):
                                    t_value = driver.find_element(by=By.XPATH, value =
                                            '//*[@id="yw1"]/table//tbody//tr['+str(tr)+']/td['+str(tc+1)+']/img[1]').get_attribute('title')
                                    nationality.append(t_value)
                                else:
                                    t_value = driver.find_element(by=By.XPATH, value =
                                                '//*[@id="yw1"]/table//tbody//tr['+str(tr)+']/td['+str(tc)+']/img[1]').get_attribute('title')
                                    nationality.append(t_value)
                                
                            if(tc == 5):
                                if(year == 2021):
                                    current_club.append(team_value)
                                else:
                                    t_value = driver.find_element(by=By.XPATH, value =
                                                '//*[@id="yw1"]/table//tbody//tr['+str(tr)+']/td['+str(tc)+']//img').get_attribute('alt')
                                    current_club.append(t_value)
                            
                            if(tc == 6):
                                market_value.append(t_value)
                                
                    
                    driver.back()
                    time.sleep(2)
                except:
                    pass
                
    #creating final DataFrame
    zipped_players = zip(p_season,team,player,p_position,birth, nationality,current_club,market_value)
    df_players = pd.DataFrame(zipped_players, columns=['season','team','player','position','birth', 'nationality','current_club','market_value'])
    print(df_players)

    driver.back()
    return(df_players)    


#running the functions  & parameters 
if (pages_limit == True):
    limit_pages = 100
else:
    limit_pages = 999999
start_year = 2015
end_year = 2021
players = scrape_players(start_year, end_year, limit_pages)
clubs = scrape_clubs(start_year, end_year)

