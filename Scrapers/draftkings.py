import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
from NFL.Game import Game as NFL_Game; 
class Draftkings():
    def __init__(self):
        self.url = "https://sportsbook.draftkings.com/"
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
    
    def get_nfl_games(self):
        self.driver.get("https://sportsbook.draftkings.com/leagues/football/nfl")

    

