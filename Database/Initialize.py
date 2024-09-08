from psycopg2 import sql
import os
from dotenv import load_dotenv
load_dotenv()

hostname = os.environ["hostname"]
username = os.environ["username"]
password = os.environ["password"]
database = "games"
port_id = os.environ["port_id"]

cursor.execute("""
    CREATE TABLE IF NOT EXISTS nfl_games (
        id SERIAL PRIMARY KEY,
        home_team VARCHAR(100),
        away_team VARCHAR(100),
        home_odds INT,
        away_odds INT,
        day INT,
        month INT,
        year INT
    );
""")
connection.commit()
