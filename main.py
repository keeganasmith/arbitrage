from Scrapers.bet365 import Bet365
from Scrapers.draftkings import Draftkings
import Database.CRUD as db
def arb(capital, a_odds, b_odds):
    a_stake = capital / (1 + a_odds / b_odds);
    b_stake = capital - a_stake;
    a_wins = a_stake * a_odds - capital;
    b_wins = b_stake * b_odds - capital;
    guarantee_profit = min(a_wins, b_wins)
    return [a_stake, b_stake, guarantee_profit]

def update_nfl_games_for_website(scraper_class):
    my_scraper = scraper_class()
    games = my_scraper.get_nfl_games()
    my_scraper.driver.quit()
    db.update_nfl_games("nfl_games", games)
if __name__ == "__main__":
    update_nfl_games_for_website(Bet365)
    update_nfl_games_for_website(Draftkings)
    #db.update_nfl_games("nfl_games", game_records)
    #result = arb(100, 2.62, 1.68)
    