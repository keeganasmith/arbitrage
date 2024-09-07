class Game:
    def __init__(self, site:str = "", home_team:str = "", away_team:str = "", home_profit:float = 0.0, away_profit:float = 0.0):
        self.site = site;
        self.home_team = home_team;
        self.away_team = away_team;
        self.home_profit = home_profit;
        self.away_profit = away_profit;
    def __str__(self):
        return f"site: {self.site}\nhome_team: {self.home_team}\naway_team: {self.away_team}\nhome_profit: {self.home_profit}\naway_profit: {self.away_profit}"