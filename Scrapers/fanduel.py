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
from common.constants import month_map
from NFL.team_mappings import team_name_abr_mapping
import pytz
from common.constants import timezone
from selenium_stealth import stealth

class Fanduel:
    def __init__(self):
        self.url = "sportsbook.fanduel.com"
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("user-data-dir=C:/Users/keegan/AppData/Local/Google/Chrome/User Data/Profile 3")
        
        self.driver = webdriver.Chrome(options=options)
        stealth(self.driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
    def get_nfl_games(self):
        self.driver.get("https://sportsbook.fanduel.com/navigation/nfl")
        wait = WebDriverWait(self.driver, 20)
        games_schedule = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="main"]/div/div[1]/div/div[2]/div[3]/ul')))
        rows = games_schedule.find_elements(By.TAG_NAME, "li")[2:]
        games = []
        for row in rows:
            try:
                teams_box = row.find_element(By.TAG_NAME, "a")
            except:
                continue
            teams_box_title = str(teams_box.get_attribute("title"))
            teams = teams_box_title.split(" @ ")
            away_team = team_name_abr_mapping[teams[0].lower()]
            home_team = team_name_abr_mapping[teams[1].lower()]
            date_box = row.find_element(By.TAG_NAME, "time")
            date_string = str(date_box.get_attribute("datetime"))
            dt = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
            dt_utc = dt.replace(tzinfo=pytz.utc)
            my_time = dt_utc.astimezone(timezone)
            day = my_time.day
            month = my_time.month
            year = my_time.year
            
            bet_buttons = row.find_elements(By.XPATH, "//*[@role='button']")
            away_money_butt = bet_buttons[1]
            home_money_butt = bet_buttons[4]
            away_odds = int(away_money_butt.text)
            home_odds = int(home_money_butt.text)
            my_game = NFL_Game(site = self.url, home_team = home_team, away_team = away_team, home_odds=home_odds, away_odds=away_odds, day = day, month = month, year = year)
            my_game.set_unique_id()
            games.append(my_game)
        return games
                        
        
        
        
        