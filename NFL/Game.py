class Game:
    def __init__(self, site:str = "", home_team:str = "", away_team:str = "", home_odds:float = 0.0, away_odds:float = 0.0):
        self.site = site;
        self.home_team = home_team;
        self.away_team = away_team;
        self.home_odds = home_odds;
        self.away_odds = away_odds;
    def __str__(self):
        return f"site: {self.site}\nhome_team: {self.home_team}\naway_team: {self.away_team}\nhome_odds: {self.home_odds}\naway_odds: {self.away_odds}"