import sqlite3
from sqlite3 import Error
import json

""" Input: Sqlite database connection
    Output: List containing shot selection data for home and away teams for each
    game in NBA history
"""
def pull_game_data(conn):
    """Send command to sqlite database to gather all historical player data"""
    cur = conn.cursor()
    cur.execute("SELECT GAME_DATE, TEAM_NAME_HOME, FGA_HOME, FG_PCT_HOME, FG3M_HOME, FG3A_HOME, FG3_PCT_HOME, TEAM_NAME_AWAY, FGA_AWAY, FG_PCT_AWAY, FG3M_AWAY, FG3A_AWAY, FG3_PCT_AWAY, WL_HOME, GAME_ID FROM Game")
    game_data = cur.fetchall()
    return game_data

"""Input: Database filepath
   Output: Connection to database
"""
def create_connection(db_file):

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connected to database")
    except Error as e:
        print(e)
        print("HOUSTON, WE HAVE A PROBLEM")

    return conn

"""Input: List containing all historical game data
   Output: game_dictionary where top level keys are unique game IDs for each
   game in NBA history
"""
def parse_game_data(game_data):
    game_dictionary = {}

    for i in game_data:
        game_date = i[0]
        game_year = i[0][0:4]
        home_team_name = i[1]
        home_fga = i[2]
        home_fg_pct = i[3]
        home_3P_made = i[4]
        home_3P_attempted = i[5]
        home_3P_pct = i[6]
        away_team_name = i[7]
        away_fga = i[8]
        away_fg_pct = i[9]
        away_3P_made = i[10]
        away_3P_attempted = i[11]
        away_3P_pct = i[12]
        WL_home = i[13]
        game_ID = i[14]

        if int(game_year) > 1975:
            game_dictionary[game_ID] = {}
            game_dictionary[game_ID]["Home Team Name"] = home_team_name
            game_dictionary[game_ID]["Home FGA"] = home_fga
            game_dictionary[game_ID]["Home FG Pct"] = home_fg_pct
            game_dictionary[game_ID]["Home 3P Made"] = home_3P_made
            game_dictionary[game_ID]["Home 3P Attempted"] = home_3P_attempted
            game_dictionary[game_ID]["Home 3P pct"] = home_3P_pct
            game_dictionary[game_ID]["Away Team Name"] = away_team_name
            game_dictionary[game_ID]["Away FGA"] = away_fga
            game_dictionary[game_ID]["Away FG Pct"] = away_fg_pct
            game_dictionary[game_ID]["Away 3P Made"] = away_3P_made
            game_dictionary[game_ID]["Away 3P Attempted"] = away_3P_attempted
            game_dictionary[game_ID]["Away 3P pct"] = away_3P_pct
            game_dictionary[game_ID]["Game Date"] = game_date
            game_dictionary[game_ID]["Game Year"] = game_year
            game_dictionary[game_ID]["WL Home"] = WL_home

        else:
            None

    return game_dictionary

#Connect to database, pull data and organize into a dictionary
database = r"full_basketball_DB.sqlite"    
conn = create_connection(database)
game_data = pull_game_data(conn)
game_dictionary = parse_game_data(game_data) 

#Write organized dictionary to json file
with open('game_data.json', 'w') as outfile:
    json.dump(game_dictionary, outfile)
