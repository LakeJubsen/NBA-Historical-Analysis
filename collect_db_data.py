import sqlite3
from sqlite3 import Error
import json

def pull_player_data(conn):
    """Send command to sqlite database to gather all historical player data"""
    cur = conn.cursor()
    cur.execute("SELECT DISPLAY_FIRST_LAST, POSITION, HEIGHT, WEIGHT, TEAM_NAME, TEAM_CITY, DRAFT_NUMBER, FROM_YEAR, PTS, AST, REB  FROM Player_Attributes")
    player_data = cur.fetchall()
    return player_data

def pull_combine_stats(conn):
    """ Send command to database to grab all players combine stats and biometrics
        If the player was not in the 'Player Attributes' table, it will add a new player"""
    cur = conn.cursor()
    cur.execute("SELECT namePlayer, wingspanInches, verticalLeapMaxInches, timeLaneAgility, timeThreeQuarterCourtSprint, repsBenchPress135 FROM Draft_Combine")
    combine_data_list = cur.fetchall()
    return combine_data_list

def add_combine_stats(player_dictionary, combine_data_list):
    """ Add combine stats to all players that are already in the player dictionary
        Players that are not already in the player dictionary will be skipped over
    """
    for i in combine_data_list:
        player_name = i[0]
        wingspan = i[1]
        vertical = i[2]
        timeLaneAgility = i[3]
        court_sprint_time = i[4]
        reps_135 = i[5]
        try:
            player_dictionary[player_name]["Wingspan"] = wingspan 
            player_dictionary[player_name]["Vertical"] = vertical 
            player_dictionary[player_name]["Time Lane Agility"] = timeLaneAgility
            player_dictionary[player_name]["Three Quarter Court Sprint Time"] = court_sprint_time
            player_dictionary[player_name]["Reps 135"] = reps_135 
        except:
            pass
    return player_dictionary


def parse_player_data(player_data_list):
    """Take list of player names and overall pick and convert to a dictionary"""
    player_dictionary = {}

    for i in player_data_list:
        player_name = i[0]
        position = i[1]
        height = i[2]
        weight = i[3]
        team = i[4]
        city = i[5]
        overall_draft_number = i[6]
        draft_year = i[7]
        ppg_avg = i[8]
        apg_avg = i[9]
        rpg_avg = i[10]

        player_dictionary[player_name] = {}
        player_dictionary[player_name]["Position"] = position
        player_dictionary[player_name]["Height"] = height
        player_dictionary[player_name]["Weight"] = weight
        player_dictionary[player_name]["Team"] = team
        player_dictionary[player_name]["City"] = city
        player_dictionary[player_name]["Overall Draft Number"] = overall_draft_number
        player_dictionary[player_name]["Draft Year"] = draft_year
        player_dictionary[player_name]["PPG AVG"] = ppg_avg
        player_dictionary[player_name]["APG AVG"] = apg_avg
        player_dictionary[player_name]["RPG AVG"] = rpg_avg

    return player_dictionary

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connected to database")
    except Error as e:
        print(e)
        print("HOUSTON, WE HAVE A PROBLEM")

    return conn


database = r"C:\Users\jakel\NBA Historical Analysis\basketball.sqlite"    
conn = create_connection(database)
player_data_list = pull_player_data(conn)
career_data_dict = parse_player_data(player_data_list)
combine_data_list = pull_combine_stats(conn)
all_player_data = add_combine_stats(career_data_dict, combine_data_list)
    
with open('player_data.json', 'w') as outfile:
    json.dump(all_player_data, outfile)
