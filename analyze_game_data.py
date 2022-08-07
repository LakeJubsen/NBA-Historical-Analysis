import json
import numpy as np
from collect_biometric_db_data import all_player_data
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


""" Input: Dictionary containing historical game data for both home and away teams
    Output: Dictionary containing averages of different shots taken by year
    Description: Simple dictionary reorganization so top-level keys are the game years
"""
def avg_stats_by_year(game_data):

    #Create empty dictionary that will contain yearly averages for different shot types
    game_year_dict = {}
    for i in range(1989, 2022):
        #print(i)
        game_year_dict[i] = {}
        game_year_dict[i]["Home FGA"] = 0
        game_year_dict[i]["Home 3P Made"] = 0
        game_year_dict[i]["Home 3P Attempted"] = 0
        game_year_dict[i]["Away FGA"] = 0
        game_year_dict[i]["Away 3P Made"] = 0
        game_year_dict[i]["Away 3P Attempted"] = 0
        game_year_dict[i]["Num Games"] = 0

    #Sum all shots of a certain type for each year
    for i in game_data:
        try:
            game_year = int(game_data[i]["Game Year"])
            home_FGA = int(game_data[i]["Home FGA"])
            home_3P_made = int(game_data[i]["Home 3P Made"])
            home_3P_attempted = int(game_data[i]["Home 3P Attempted"])
            
            away_FGA = int(game_data[i]["Away FGA"])
            away_3P_made = int(game_data[i]["Away 3P Made"])
            away_3P_attempted = int(game_data[i]["Away 3P Attempted"])

            game_year_dict[game_year]["Home FGA"] += home_FGA
            game_year_dict[game_year]["Home 3P Made"] += home_3P_made
            game_year_dict[game_year]["Home 3P Attempted"] += home_3P_attempted
            game_year_dict[game_year]["Away FGA"] += away_FGA
            game_year_dict[game_year]["Away 3P Made"] += away_3P_made
            game_year_dict[game_year]["Away 3P Attempted"] += away_3P_attempted
            game_year_dict[game_year]["Num Games"] += 1
        except:
            pass
    
    #Divide sum of shots of a certain type by number of games played to get averages
    for i in range(1989,2022):
        game_year_dict[i]["Home FGA"] /= game_year_dict[i]["Num Games"] 
        game_year_dict[i]["Home 3P Made"] /= game_year_dict[i]["Num Games"] 
        game_year_dict[i]["Home 3P Attempted"] /= game_year_dict[i]["Num Games"] 
        game_year_dict[i]["Away FGA"] /= game_year_dict[i]["Num Games"] 
        game_year_dict[i]["Away 3P Made"] /= game_year_dict[i]["Num Games"] 
        game_year_dict[i]["Away 3P Attempted"] /= game_year_dict[i]["Num Games"] 

        game_year_dict[i]["Home FGA"] = round(game_year_dict[i]["Home FGA"],2)
        game_year_dict[i]["Home 3P Made"] = round(game_year_dict[i]["Home 3P Made"],2)
        game_year_dict[i]["Home 3P Attempted"] = round(game_year_dict[i]["Home 3P Attempted"],2)
        game_year_dict[i]["Away FGA"] = round(game_year_dict[i]["Away FGA"],2)
        game_year_dict[i]["Away 3P Made"] =round(game_year_dict[i]["Away 3P Made"],2)
        game_year_dict[i]["Away 3P Attempted"] = round(game_year_dict[i]["Away 3P Attempted"], 2)

    return game_year_dict

""""Input: Dictionary of home and away team shot selection per year
    Output: Two plots...
        1. Number of 3 point attempts per year 
        2. Three point attempt, three pointers made, field goal attempts correlation with win probability
    Description: Converts data from dictionary into lists for plotting
    """
def plot_shot_selection_by_year(game_year_dict):
    game_years = np.arange(1989,2022)

    away_3pm = []
    away_3pa = []
    away_fga = []

    home_3pm = []
    home_3pa = []
    home_fga = []

    total_3pm = []
    total_3pa = []
    total_fga = []

    for i in range(1989, 2022):
        home_3pm.append(game_year_dict[i]["Home 3P Made"])
        home_3pa.append(game_year_dict[i]["Home 3P Attempted"])
        home_fga.append(game_year_dict[i]["Home FGA"])
        away_3pm.append(game_year_dict[i]["Away 3P Made"])
        away_3pa.append(game_year_dict[i]["Away 3P Attempted"])
        away_fga.append(game_year_dict[i]["Away FGA"])

        total_3pm.append(game_year_dict[i]["Home 3P Made"] + game_year_dict[i]["Away 3P Made"])
        total_3pa.append(game_year_dict[i]["Home 3P Attempted"] + game_year_dict[i]["Away 3P Attempted"])
        total_fga.append(game_year_dict[i]["Home FGA"] + game_year_dict[i]["Away FGA"])


    fig1 = go.Figure()
    #Home team plots
    fig1.add_trace(go.Scatter(x = game_years, y = total_3pm, name = 'Total 3 Pointers Made', line = dict(color='firebrick', width = 3, dash = 'dot')))
    fig1.add_trace(go.Scatter(x = game_years, y = total_3pa, name = 'Total 3 Pointers Attempted', line = dict(color='firebrick', width = 3, dash = 'dash')))
    fig1.add_trace(go.Scatter(x = game_years, y = total_fga, name = 'Total Field goal attempts', line = dict(color='firebrick', width = 3)))

    #Formatting
    fig1.update_layout(title = 'NBA Shot Selection by Year', xaxis_title = 'Year', yaxis_title = 'Shots',
        xaxis = dict(
            tickmode = 'linear', 
            tick0 = 1989, 
            dtick = 1
        ),
        yaxis = dict(
            tickmode = 'linear',
            tick0 = 0,
            dtick = 5
        )
    )
    fig1.show()
""""Input: Dictionary containing historical game data
    Output: Three dictionaries containing data relating home team vs away team shot selection
    and win probability.
    Description: Want to find if there is a correlation between home vs away team shot selection (three point attempts (TPA),
    three pointers made (TPM), field goal attempts (FGA)) and which team wins. The function subtracts the difference between home vs away
    TPA, TPM, FGA and correlates the differential with win probability for the home team.
    """
def calculate_win_pct(game_data):
    TPA_diff_dict = {}
    TPM_diff_dict = {}
    FGA_diff_dict = {}

    for i in game_data:
        #Filter out all games before 1989 for robust data - database does not contain full dataset for all year
        if int(game_data[i]["Game Year"]) > 1988:
            game_result = game_data[i]["WL Home"];
            TPA_diff = int(game_data[i]["Home 3P Attempted"]) - int(game_data[i]["Away 3P Attempted"])
            TPM_diff = int(game_data[i]["Home 3P Made"]) - int(game_data[i]["Away 3P Made"])
            FGA_diff = int(game_data[i]["Home FGA"]) - int(game_data[i]["Away FGA"])

            """Need to figure out a more efficient way of doing this...
            The following series of if statements parse """
            if TPA_diff not in TPA_diff_dict:
                TPA_diff_dict[TPA_diff] = {}
                TPA_diff_dict[TPA_diff]["Wins"] = 0
                TPA_diff_dict[TPA_diff]["Losses"] = 0

            if TPM_diff not in TPM_diff_dict:
                TPM_diff_dict[TPM_diff] = {}
                TPM_diff_dict[TPM_diff]["Wins"] = 0
                TPM_diff_dict[TPM_diff]["Losses"] = 0

            if FGA_diff not in FGA_diff_dict:
                FGA_diff_dict[FGA_diff] = {}
                FGA_diff_dict[FGA_diff]["Wins"] = 0
                FGA_diff_dict[FGA_diff]["Losses"] = 0

            if game_result == 'W':
                TPA_diff_dict[TPA_diff]["Wins"] += 1
                TPM_diff_dict[TPM_diff]["Wins"] += 1
                FGA_diff_dict[FGA_diff]["Wins"] += 1

            elif game_result == 'L':
                TPA_diff_dict[TPA_diff]["Losses"] += 1
                TPM_diff_dict[TPM_diff]["Losses"] += 1
                FGA_diff_dict[FGA_diff]["Losses"] += 1
            else:
                None
        else:
            None

    #Calculates win percentage of home team at each shot selection differential
    for i in TPM_diff_dict:
        TPM_diff_dict[i]["Win PCT"] = TPM_diff_dict[i]["Wins"] / (TPM_diff_dict[i]["Wins"] + TPM_diff_dict[i]["Losses"])
    for i in TPA_diff_dict:
        TPA_diff_dict[i]["Win PCT"] = TPA_diff_dict[i]["Wins"] / (TPA_diff_dict[i]["Wins"] + TPA_diff_dict[i]["Losses"])
    for i in FGA_diff_dict:
        FGA_diff_dict[i]["Win PCT"] = FGA_diff_dict[i]["Wins"] / (FGA_diff_dict[i]["Wins"] + FGA_diff_dict[i]["Losses"])        
    
    #Sort so differentials are organized in ascending order
    FGA_diff_dict = dict(sorted(FGA_diff_dict.items()))
    TPM_diff_dict = dict(sorted(TPM_diff_dict.items()))
    TPA_diff_dict = dict(sorted(TPA_diff_dict.items()))

    return FGA_diff_dict, TPA_diff_dict, TPM_diff_dict

""" Input: Three dictionaries containing differential between home and away team's
    field goal attempts (FGA), three point attempts (TPA) and three pointers made (TPM)
    Output: Plotly graphs finding correlation between win percentage and FGA, TPA, TPM
    Description: This function takes the three input dictionaries and organizes the data
    in a way that can be plotted easily using plotly."""
def plot_win_pct(FGA_diff_dict, TPA_diff_dict, TPM_diff_dict):
    TPM_diff_list = []
    TPM_value_list = []
    TPA_diff_list = []
    TPA_value_list = []
    FGA_diff_list = []
    FGA_value_list = []
    for i in TPM_diff_dict:
        TPM_diff_list.append(i)
        TPM_value_list.append(TPM_diff_dict[i]["Win PCT"])
    for i in TPA_diff_dict:
        if i < 20 and i > -20:
            TPA_diff_list.append(i)
            TPA_value_list.append(TPA_diff_dict[i]["Win PCT"])
        else:
            None
    for i in FGA_diff_dict:
        if i < 20 and i > -20:
            FGA_diff_list.append(i)
            FGA_value_list.append(FGA_diff_dict[i]["Win PCT"])
        else:
            None

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x = TPM_diff_list, y = TPM_value_list, 
        name = '3-Point Made Differential', 
        line = dict(color='firebrick', 
        width = 3, 
        dash = 'dot')))
    fig2.add_trace(go.Scatter(x = TPA_diff_list, y = TPA_value_list, 
        name = '3-Point Attempt Differential', 
        line = dict(color='firebrick', 
        width = 3, 
        dash = 'dash')))
    fig2.add_trace(go.Scatter(x = FGA_diff_list, y = FGA_value_list, 
        name = 'Field Goal Attempt Differential', 
        line = dict(color='royalblue', 
        width = 3, )))

    #Formatting
    fig2.update_layout(title = 'NBA Win Percentage Based on Shot Selection', xaxis_title = 'Difference Between Home Team vs Away Team Shots', yaxis_title = 'Home Team Win Percent',
        xaxis = dict(
            tickmode = 'linear', 
            tick0 = -15, 
            dtick = 1
        ),
        yaxis = dict(
            tickmode = 'linear',
            tick0 = 0,
            dtick = 0.05
        )
    )
    fig2.show()

#Load data from json file
f = open(r'game_data.json','r')
game_data = json.load(f)

#Calculate and plot shot selection by year
game_year_dict = avg_stats_by_year(game_data)
plot_shot_selection_by_year(game_year_dict)

#Calculate and plot correlation between win % and FGA, TPA, TPM
FGA_diff_dict, TPA_diff_dict, TPM_diff_dict = calculate_win_pct(game_data)
plot_win_pct(FGA_diff_dict, TPA_diff_dict, TPM_diff_dict)
