import json
import numpy as np
from collect_biometric_db_data import all_player_data
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

""" Input: Dictionary containing all player data
    Output: Dictionary containing player heights and weights oranized by draft year
"""
def height_weight_by_year(player_data):
    first_year = 1946
    last_year = 2022
    
    height_weight_year_dict = {}
    for i in range(first_year, last_year):
        height_weight_year_dict[i] = {}
        height_weight_year_dict[i]["Height"] = []
        height_weight_year_dict[i]["Weight"] = []

    for i in player_data:
        try:
            height = float(player_data[i]["Height"])
            weight = float(player_data[i]["Weight"])
            draft_year = int(player_data[i]["Draft Year"])
            height_weight_year_dict[draft_year]["Height"].append(height)
            height_weight_year_dict[draft_year]["Weight"].append(weight)
        except:
            pass
    return height_weight_year_dict

""" Input: Dictionary containing all player data
    Output: Dictionary containing player verticals oranized by draft year
"""
def vertical_by_year(player_data):
    vertical_year_dict = {}
    for i in range(2001, 2019):
        vertical_year_dict[i] = {}
        vertical_year_dict[i]["Vertical"] = []

    for i in player_data:
        try:
            vertical = float(player_data[i]["Vertical"])
            draft_year = int(player_data[i]["Draft Year"])
            vertical_year_dict[draft_year]["Vertical"].append(vertical)
        except:
            pass
    return vertical_year_dict

""" Input: Dictionary containing player verticals oranized by draft year
    Output: List containing average vertical values corresponding to each draft year
"""
def avg_vertical_by_year(vertical_by_year):
    avg_vertical_dict = {}
    avg_vertical_list =[]
    for i in range(2001, 2019):
        avg_vertical_dict[i] = {}
        avg_vertical_dict[i]["Vertical"] = {}
    for i in vertical_by_year:
        avg_vert = sum(vertical_by_year[i]["Vertical"])/len(vertical_by_year[i]["Vertical"])
        avg_vertical_dict[i]["Vertical"] = avg_vert
        avg_vertical_list.append(avg_vert)

    return avg_vertical_list

""" Input: Dictionary containing player heights and weights oranized by draft year
    Output: 2 Lists containing average height and weight values corresponding to each draft year
"""
def avg_height_weight_by_year(height_weight_by_year):
    avg_height_dict = {}
    avg_height_list =[]
    avg_weight_dict = {}
    avg_weight_list = []
    for i in range(1946, 2020):
        avg_weight_dict[i] = {}
        avg_weight_dict[i]["Weight"] = {}
        avg_height_dict[i] = {}
        avg_height_dict[i]["Height"] = {}

    for i in height_weight_by_year:

        try:
            avg_weight = sum(height_weight_by_year[i]["Weight"])/len(height_weight_by_year[i]["Weight"])
            avg_height = sum(height_weight_by_year[i]["Height"])/len(height_weight_by_year[i]["Height"])

            avg_weight_dict[i]["Weight"] = avg_weight
            avg_weight_list.append(avg_weight)
            avg_height_dict[i]["Height"] = avg_height
            avg_height_list.append(avg_height)
        except:
            pass

    return avg_height_list, avg_weight_list

""" Input: Lists containing average vertical, height and weight corresponding to draft year
    Output: Plots of draft year vs average vertical, height and weight"""
def plot_all(avg_vertical, avg_height, avg_weight):
    vert_years = np.arange(2001,2019)
    height_weight_years = np.arange(1945,2019)
    
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x = vert_years, y = avg_vertical, name = 'Vertical', line = dict(color='firebrick', width = 3)))
    fig1.update_layout(title = 'Average NBA Player Vertical by Year', xaxis_title = 'Year', yaxis_title = 'Vertical (in)')
    fig1.show()

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x = height_weight_years, y = avg_height, name = 'Height', line = dict(color='firebrick', width = 3, dash = 'dot')))
    fig2.update_layout(title = 'Average NBA Player Height by Year', xaxis_title = 'Year', yaxis_title = 'Height (in)')
    fig2.show()

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x = height_weight_years, y = avg_weight, name = 'Weight', line = dict(color='royalblue', width = 3, dash = 'dot')))
    fig3.update_layout(title = 'Average NBA Player Weight by Year', xaxis_title = 'Year', yaxis_title = 'Weight (lbs)')
    fig3.show()


f = open(r'player_data.json','r')
player_data = json.load(f)

vertical_by_year = vertical_by_year(player_data)
height_weight_by_year = height_weight_by_year(player_data)

avg_verticals = avg_vertical_by_year(vertical_by_year)
avg_heights, avg_weights = avg_height_weight_by_year(height_weight_by_year)

plot_all(avg_verticals, avg_heights, avg_weights)


