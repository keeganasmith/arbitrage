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
import undetected_chromedriver as uc
from common.constants import month_map
class Betonline:
    def __init__(self):
        self.mapping = team_name_abr_mapping();
        self.url = "sports.betonline.ag"
        chrome_options = Options()
        #chrome_options.add_argument("--headless=new")
        #chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--remote-debugging-port=9222")
        #chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")


        self.driver = uc.Chrome(options=chrome_options)
    
    def get_nfl_games(self):
        self.driver.get("https://sports.betonline.ag/sportsbook/football/nfl")
        wait = WebDriverWait(self.driver, 10)
        table = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".content-league-container")))
        rows = table.find_elements(By.CSS_SELECTOR, ".event-row-container")
        games = []
        for row in rows:
            date = row.find_element(By.CSS_SELECTOR, '[data-testid="date-text-id"]').text
            month = str(month_map[date.split(" ")[0].lower()])
            day = date.split(" ")[1][:-1]
            year = datetime.now().year
            if(datetime.now().month > int(month)):
                year += 1
            participant_boxes = row.find_elements(By.CSS_SELECTOR, '[data-testid="participant-name"]');
            away_full_name = str(participant_boxes[0].text).lower()
            home_full_name = str(participant_boxes[1].text).lower()
            away_name = self.mapping[away_full_name]
            home_name = self.mapping[home_full_name]
            spreads = row.find_element(By.CSS_SELECTOR, ".markets-container")
            containers = spreads.find_elements(By.CSS_SELECTOR, '[data-testid="vertical-market-type"]')
            moneyline_container = containers[1]
            odds = moneyline_container.find_elements(By.CSS_SELECTOR, '.odd')
            away_odds = int(odds[0].text)
            home_odds = int(odds[1].text)
            mygame = NFL_Game(self.url, home_name, away_name, home_odds, away_odds, day, month, year)
            mygame.set_unique_id()
            games.append(mygame)
        return games



