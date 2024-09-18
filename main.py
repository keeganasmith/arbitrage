from Scrapers.bet365 import Bet365
from Scrapers.draftkings import Draftkings
from Scrapers.betmgm import Betmgm
from  Scrapers.betonline import Betonline
from Scrapers.williamhill import Williamhill
import Database.CRUD as db
import concurrent.futures

def arb(capital, a_odds, b_odds):
    a_stake = capital / (1 + a_odds / b_odds);
    b_stake = capital - a_stake;
    a_wins = a_stake * a_odds - capital;
    b_wins = b_stake * b_odds - capital;
    guarantee_profit = min(a_wins, b_wins)
    return [a_stake, b_stake, guarantee_profit]
def convert_american_to_odds(american_odds):
    if(american_odds >= 0):
        return 1.0 + american_odds / 100.0
    return 1.0 + (100.0 / abs(american_odds))
def find_arb_opps_nfl():
    grouped_nfl_games = db.groupby("nfl_games", "shared_id")
    previous_id = grouped_nfl_games[0]["shared_id"]
    i = 1;
    current_home_max = convert_american_to_odds(grouped_nfl_games[0]["home_odds"])
    home_max_site = grouped_nfl_games[0]["site"]
    current_away_max = convert_american_to_odds(grouped_nfl_games[0]["away_odds"])
    away_max_site = grouped_nfl_games[0]["site"]
    while(i < len(grouped_nfl_games)):
        game = grouped_nfl_games[i]
        game_home_odds = convert_american_to_odds(game["home_odds"])
        game_away_odds = convert_american_to_odds(game["away_odds"])
        if(game["shared_id"] != previous_id):
            arb_opp = arb(100, current_home_max, current_away_max)
            print(f"The arb opp for {previous_id} is ", arb_opp, f" home site: {home_max_site}, away site: {away_max_site}")
            current_home_max = 0.0
            current_away_max = 0.0
        if(game_home_odds > current_home_max):
            current_home_max = game_home_odds
            home_max_site = game["site"]
        if(game_away_odds > current_away_max):
            current_away_max = game_away_odds
            away_max_site = game["site"]
        previous_id = game["shared_id"]
        i += 1
        

def update_nfl_games_for_website(scraper_class):
    my_scraper = scraper_class()
    games = my_scraper.get_nfl_games()
    my_scraper.driver.quit()
    db.update_nfl_games("nfl_games", games)
if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor() as executor:
        scrapers = [Bet365, Draftkings, Betmgm, Betonline, Williamhill]
        futures = []
        for i in range(0, len(scrapers)):
            futures.append(executor.submit(update_nfl_games_for_website, scrapers[i]));
        for future in concurrent.futures.as_completed(futures):
            future.result()

    find_arb_opps_nfl()
    