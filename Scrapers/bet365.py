import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        name_containers = game_name_column.find_elements(By.TAG_NAME, "div")
        team_name_div_class = "sac-ParticipantFixtureDetailsHigherAmericanFootball "
        #sac-ParticipantFixtureDetailsHigherAmericanFootball sac-StylingRCAmericanModule_Width-0 rcl-MarketCouponAdvancedBase_Divider gl-Market_General-cn1 sac-ParticipantFixtureDetailsHigherAmericanFootball-wide
        date_div_class = "rcl-MarketHeaderLabel rcl-MarketHeaderLabel-isdate"
        month = 0;
        day = 0;
        games = []
        now = datetime.now()
        year = now.year
        for div in name_containers:
            div_class = div.get_attribute("class").strip()
            if(div_class == date_div_class):
                date_list = div.text.split(" ")
                new_month = month_map[date_list[1]]
                if(new_month < month):
                    year += 1
                month = new_month
                day = int(date_list[2])
            if(team_name_div_class in div_class):
                team_names = div.find_elements(By.CSS_SELECTOR, ".sac-ParticipantFixtureDetailsHigherAmericanFootball_Team")
                if(len(team_names) < 2):
                    continue
                away_team = team_names[0].text
                home_team = team_names[1].text
                games.append(NFL_Game(site = self.url, home_team = home_team, away_team = away_team, day = day, month = month, year = year))
        print("games length", len(games))
        # for container in name_containers:
        #     team_names = container.find_elements(By.CSS_SELECTOR, ".sac-ParticipantFixtureDetailsHigherAmericanFootball_Team")
        #     away_team = team_names[0].text
        #     home_team = team_names[1].text
        #     games.append(NFL_Game(site = self.url, home_team = home_team, away_team = away_team))
        spread_columns = game_grid.find_elements(By.CSS_SELECTOR, ".sgl-MarketOddsExpand")
        money_column = spread_columns[2]
        odds_elements = money_column.find_elements(By.CSS_SELECTOR, ".sac-ParticipantOddsOnly50OTB_Odds")
        i = 0
        while(i < len(odds_elements) - 1):
            away_odds = odds_elements[i].text
            home_odds = odds_elements[i+1].text
            games[i // 2].home_odds = home_odds
            games[i // 2].away_odds = away_odds
            i += 2
        return games
