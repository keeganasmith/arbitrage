import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
class Bet365:
    def __init__(self):
        self.url = "https://www.la.bet365.com/"
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
    
    def get_nfl_games(self):
        wait = WebDriverWait(self.driver, 10)

        sport_ribbon = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".crm-ClassificationRibbonModule_CompetitionScrollerContainer")))
        nfl_button = sport_ribbon.find_element(By.XPATH, "//*[text()='NFL']")
        nfl_button.click()
        game_container = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".cm-CouponMarketGroup")))
        game_grid = game_container.find_element(By.CSS_SELECTOR, ".gl-MarketGroupContainer")
        game_name_column = game_grid.find_element(By.CSS_SELECTOR, ".sgl-MarketFixtureDetailsLabel")
        name_containers = game_name_column.find_elements(By.CSS_SELECTOR, ".sac-ParticipantFixtureDetailsHigherAmericanFootball_TeamNames")
        
        for container in name_containers:
            team_names = container.find_elements(By.CSS_SELECTOR, ".sac-ParticipantFixtureDetailsHigherAmericanFootball_Team")
            home_team = team_names[0].text
            away_team = team_names[1].text
            print("home: ", home_team, " away: ", away_team)