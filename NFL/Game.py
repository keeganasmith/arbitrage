class Game:
    def __init__(self, site:str = "", home_team:str = "", away_team:str = "", home_odds:int = 0, away_odds:int = 0, day: int = 0, month:int = 0, year:int = 0, unique_id:str = ""):
        self.site = site;
        self.home_team = home_team;
        self.away_team = away_team;
        self.home_odds = home_odds;
        self.away_odds = away_odds;
        self.day = day;
        self.month = month;
        self.year = year
        self.unique_id = unique_id
    def __dict__(self):
        return {
            "site": self.site,
            "home_team": self.home_team,
            "away_team": self.away_team,
            "home_odds" : self.home_odds,
            "away_odds" : self.away_odds,
            "day" : self.day,
            "month": self.month,
            "year" : self.year,
            "unique_id" : self.unique_id
        }
    def __str__(self):
        return f"site: {self.site}\nhome_team: {self.home_team}\naway_team: {self.away_team}\nhome_odds: {self.home_odds}\naway_odds: {self.away_odds}\ndate: {self.month}/{self.day}/{self.year}"