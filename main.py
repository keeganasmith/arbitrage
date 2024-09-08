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
if __name__ == "__main__":
    my_draft_kings = Draftkings()
    draft_king_records = my_draft_kings.get_nfl_games()
    my_draft_kings.driver.quit()
    db.update_nfl_games("nfl_games", draft_king_records)
    my_bet365 = Bet365()
    bet365_records = my_bet365.get_nfl_games()
    db.update_nfl_games("nfl_games", bet365_records)
    my_bet365.driver.quit()
    #db.update_nfl_games("nfl_games", game_records)
    #result = arb(100, 2.62, 1.68)
    