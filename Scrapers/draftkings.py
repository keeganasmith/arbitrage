import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime, timedelta
from NFL.Game import Game as NFL_Game; 
month_map = {
    "jan" : 1,
    "feb" : 2,
    "mar" : 3,
    "apr" : 4,
    "may" : 5,
    "jun" : 6,
    "jul" : 7,
    "aug" : 8,
    "sep" : 9,
    "oct" : 10,
    "nov" : 11,
    "dec" : 12
}
def first_num(my_string):
    result = ""
    for i in range(0, len(my_string)):
        if(ord(my_string[i]) >= 48 and ord(my_string[i]) <= 57):
            result += my_string[i]
        else:
            break;
    return result
class Draftkings():
    def __init__(self):
        self.url = "https://sportsbook.draftkings.com/"
        
        self.driver = webdriver.Chrome()
    
    def get_nfl_games(self):
        self.driver.get("https://sportsbook.draftkings.com/leagues/football/nfl")
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.sportsbook-table__body')))
        tables = self.driver.find_elements(By.CSS_SELECTOR, '.sportsbook-table')
        print(f"there are {len(tables)} tables")
        now = datetime.now()
        games = []

        for table in tables:
            header_content = table.find_element(By.CSS_SELECTOR, ".sportsbook-table-header__title").text
            #Handling dates and whatnot
            day = 0;
            month = 0;
            year = 0;
            
            if("TODAY" in header_content):
                day = now.day
                month = now.month
                year = now.year
            elif("TOMORROW" in header_content):
                tomorrow = now + timedelta(days = 1)
                day = tomorrow.day
                month = tomorrow.month
                year = tomorrow.year
            else:
                date_string = header_content.split(" ")
                day = int(first_num(date_string[-1]));
                raw_month = date_string[1].lower()
                month = month_map[raw_month]
                if(month < now.month):
                    year = now.year + 1
                else:
                    year = now.year
            
            #handling games
            rows = table.find_elements(By.TAG_NAME, 'tr')
            i = 1
            my_game = None
            while(i < len(rows)):
                row = rows[i]
                if(i % 2 == 1):
                    my_game = NFL_Game()
                    column = row.find_element(By.CSS_SELECTOR, ".sportsbook-table__column-row")
                    my_game.away_team = row.find_element(By.CSS_SELECTOR, ".event-cell__name-text").text.split(" ")[0]
                    try:
                        odds_text = row.find_elements(By.TAG_NAME, "td")[2].find_element(By.TAG_NAME, "span").text
                        odds_text = odds_text.replace('−', '-')
                        my_game.away_odds = int(odds_text)
                        my_game.day = day;
                        my_game.month = month;
                        my_game.year = year
                        my_game.site = self.url
                    except Exception as e:
                        print("couldn't find the odds for this game")
                        my_game = None
                        i += 1
                else:
                    try:
                        my_game.home_team = row.find_element(By.CSS_SELECTOR, ".event-cell__name-text").text.split(" ")[0]
                        odds_text = row.find_elements(By.TAG_NAME, "td")[2].find_element(By.TAG_NAME, "span").text
                        odds_text = odds_text.replace('−', '-')
                        my_game.home_odds = int(odds_text)
                        my_game.set_unique_id()
                        print(f"odds for game: {my_game.away_team} at {my_game.home_team} is {my_game.away_odds} - {my_game.home_odds}")
                        games.append(my_game)
                    except Exception as e:
                        print("couldn't find the odds for this game")
                        my_game = None;

                    
                i += 1
        return games
            

                




