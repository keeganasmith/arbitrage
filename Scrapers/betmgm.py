import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from NFL.team_mappings import team_mascot_abr_mapping
import time
from datetime import datetime
from NFL.Game import Game as NFL_Game; 
month_map = {
    "Jan" : 1,
    "Feb" : 2,
    "Mar" : 3,
    "Apr" : 4,
    "May" : 5,
    "Jun" : 6,
    "Jul" : 7,
    "Aug" : 8,
    "Sep" : 9,
    "Oct" : 10,
    "Nov" : 11,
    "Dec" : 12
}
class Betmgm:
    def __init__(self):
        self.url = "https://sports.az.betmgm.com"
        chrome_options = Options()
        #chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1920,1080")
        # chrome_options.add_argument("--no-sandbox")
        self.mascot_map = team_mascot_abr_mapping();
        self.driver = webdriver.Chrome(options=chrome_options)

    def get_nfl_games(self):
        self.driver.get("https://sports.az.betmgm.com/en/sports/football-11/betting/usa-9/nfl-35")
        wait = WebDriverWait(self.driver, 10)
        grid = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".six-pack-groups")))
        rows = grid.find_elements(By.TAG_NAME, "ms-six-pack-event")
        games = []
        for row in rows:
            date = str(row.find_element(By.TAG_NAME, "ms-prematch-timer").text).split(" ")[0];
            date = date.split("/")
            day = date[1]
            month = date[0]
            year = "20" + date[2]
            teams_names = row.find_elements(By.CSS_SELECTOR, ".participant")
            away_mascot = str(teams_names[0].text).lower()
            home_mascot = str(teams_names[1].text).lower()

            away_name = self.mascot_map[away_mascot]
            home_name = self.mascot_map[home_mascot]
            spread_groups = row.find_elements(By.TAG_NAME, "ms-option-group")
            money_groups = spread_groups[2].find_elements(By.TAG_NAME, "span")
            away_money = money_groups[0].text;
            home_money = money_groups[1].text;
            my_game = NFL_Game(self.url, home_name, away_name, home_money, away_money, day, month, year)
            my_game.set_unique_id();
            games.append(my_game)
        return games
            
        