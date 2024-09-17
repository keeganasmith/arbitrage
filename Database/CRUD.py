import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv
from NFL.Game import Game
from deepdiff import DeepDiff
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
def get_column_names(table_name):
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM {table_name} LIMIT 1;")
    column_names = [desc[0] for desc in cursor.description]
    return column_names
def retrieve_records(table_name):
    cursor = connection.cursor()

    select_query = f"SELECT * FROM {table_name};"
    cursor.execute(select_query)
    return cursor.fetchall()
def convert_query_result_to_dicts(table, query_result):
    column_names = get_column_names(table)
    result = []
    for row in query_result:
        my_dict = dict(zip(column_names, row))
        result.append(my_dict)
    return result
def groupby(table_name, column):
    cursor = connection.cursor()
    select_query = f'''SELECT *
    FROM {table_name}
    WHERE {column} IN (
        SELECT {column}
        FROM {table_name}
        GROUP BY {column}
        HAVING COUNT(*) > 1
    )
    ORDER BY shared_id;'''
    cursor.execute(select_query);
    query_result = cursor.fetchall()
    return convert_query_result_to_dicts(table_name, query_result)
def insert_object(table, record):
    cursor = connection.cursor()

    object_dict = record.__dict__()
    columns = ', '.join(object_dict.keys()) 
    values = tuple(object_dict.values())    
    placeholders = ', '.join(['%s'] * len(values))
    insert_query = f'''
    INSERT INTO {table} ({columns})
    VALUES ({placeholders});
    '''
    cursor.execute(insert_query, values)
    connection.commit()
def insert_objects(table, records):
    cursor = connection.cursor()

    object_dict = records[0].__dict__()
    columns = ', '.join(object_dict.keys()) 
    placeholders = ', '.join(['%s'] * len(object_dict.keys()))
    insert_query = f'''
    INSERT INTO {table} ({columns})
    VALUES ({placeholders});
    '''
    values = []
    for value in records:
        values.append(tuple(value.__dict__().values()))    
    cursor.executemany(insert_query, values)
    connection.commit()

def update_nfl_games(table, game_records):
    cursor = connection.cursor()

    all_games = retrieve_records(table)
    db_unique_id_map = {}
    column_names = get_column_names(table)
    for game in all_games:
        my_game = dict(zip(column_names, game))
        db_unique_id_map[my_game["unique_id"]] = my_game
    delete_ids = []
    records_to_not_insert = set()
    for game in game_records:
        my_game_id = game.unique_id
        if(my_game_id in db_unique_id_map):
            diff = DeepDiff(game.__dict__(), db_unique_id_map[my_game_id])
            if(diff != {}):
                delete_ids.append(my_game_id)
            else:
                records_to_not_insert.add(my_game_id)
    #DELETE records which need to be updated
    if(len(delete_ids) != 0):
        delete_id_tup = tuple(delete_ids)
        placeholders = ', '.join(['%s'] * len(delete_ids))
        delete_query = f"DELETE FROM {table} WHERE unique_id IN ({placeholders});"
        cursor.execute(delete_query, delete_id_tup)

    #INSERT records, except for ones that already exist
    games_to_insert = []
    for game in game_records:
        if(not (game.unique_id in records_to_not_insert)):
            games_to_insert.append(game)
    insert_objects(table, games_to_insert)



