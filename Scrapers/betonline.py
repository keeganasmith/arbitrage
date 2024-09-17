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
from NFL
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
class Betonline(self):
    def __init__(self):
        self.url = "sports.betonline.ag"
        self.driver = webdriver.Chrome()
    
    def get_nfl_games(self):
        self.driver.get("https://sports.betonline.ag/sportsbook/football/nfl")
        wait = WebDriverWait(10, self.driver)
        table = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".content-league-container")))
        rows = table.find_element(By.CSS_SELECTOR, ".event-row-container")
        for row in rows:



