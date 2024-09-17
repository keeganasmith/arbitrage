import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv
load_dotenv()

hostname = os.environ["hostname"]
username = os.environ["user"]
password = os.environ["password"]
database = "games"
port_id = os.environ["port_id"]
connection = psycopg2.connect(
    host=hostname,
    dbname=database,
    user=username,
    password=password,
    port=port_id
)

cursor = connection.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS nfl_games (
        id SERIAL PRIMARY KEY,
        site VARCHAR(100),
        home_team VARCHAR(100),
        away_team VARCHAR(100),
        home_odds INT,
        away_odds INT,
        day INT,
        month INT,
        year INT,
        unique_id VARCHAR(100),
        shared_id VARCHAR(100)
    );
""")

connection.commit()
