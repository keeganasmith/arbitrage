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
from NFL.team_mappings import team_name_abr_mapping
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

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
class Williamhill:
    def __init__(self):
        self.mapping = team_name_abr_mapping();
        self.url = "williamhill.us"
        chrome_options = Options()
        #chrome_options.add_argument("--headless=new")
        #chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--window-size=1920,1080")
        #chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        self.driver = webdriver.Chrome(options=chrome_options)
    def try_to_click_thing(self, condition, tries=3):
        wait = WebDriverWait(self.driver, 4)
        for i in range(0, tries):
            try:
                thing = wait.until(EC.visibility_of_element_located(condition))
                thing.click()
                break;
            except StaleElementReferenceException:
                if i < tries - 1:
                    print(f"Attempt {i+1} failed, retrying...")
                    continue  # Retry finding and clicking the button
                else:
                    print("Max retries reached, unable to click the football button due to stale element.")
                    raise
            except TimeoutException:
                print("Football button not found within the time limit.")
                raise

        
    def get_nfl_games(self):
        self.driver.get("https://williamhill.us/us/nv/bet?dl=retail_mode")    
        wait = WebDriverWait(self.driver, 10)
        self.try_to_click_thing((By.XPATH, '//div[@class="ListContent" and @data-qa="football"]'))
        nfl_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="ListContent" and @data-qa="nfl"]')))
        nfl_button.click()
        schedule_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="pill-title" and @data-qa="pill-schedule"]')))
        schedule_button.click()
        schedule_container = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".eventList")))
        cards = schedule_container.find_elements(By.CSS_SELECTOR, ".EventCard")
        games = []
        for card in cards:
            date_container = card.find_element(By.CSS_SELECTOR, ".dateContainer")
            date = str(date_container.text).split(" ")
            month = month_map[date[0].lower()]
            day = int(date[1])
            year = datetime.now().year
            if(month < datetime.now().month):
                year += 1
            teams = card.find_elements(By.CSS_SELECTOR, ".competitor")
            away_team = str(teams[0].text).lower()
            home_team = str(teams[1].text).lower()
            away_team = self.mapping[away_team]
            home_team = self.mapping[home_team]
            money_lines = card.find_elements(By.CSS_SELECTOR, ".col3")[1:]
            away_odds = int(str(money_lines[0].text))
            home_odds = int(str(money_lines[1].text))
            
            mygame = NFL_Game(self.url, home_team, away_team, home_odds, away_odds, day, month, year)
            mygame.set_unique_id()
            games.append(mygame)
        return games