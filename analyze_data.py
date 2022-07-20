import json
import numpy as np
from collect_db_data import all_player_data
import matplotlib.pyplot as plt

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

def plot_vertical_by_year(vertical_by_year):
    avg_vertical_dict = {}
    avg_vertical_list =[]
    for i in range(2001, 2019):
        avg_vertical_dict[i] = {}
        avg_vertical_dict[i]["Vertical"] = {}
    for i in vertical_by_year:
        avg_vert = sum(vertical_by_year[i]["Vertical"])/len(vertical_by_year[i]["Vertical"])
        avg_vertical_dict[i]["Vertical"] = avg_vert
        avg_vertical_list.append(avg_vert)
        print(avg_vert)
        print(i)

    return avg_vertical_list


def plot_height_weight_by_year(height_weight_by_year):
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

def plot_all(avg_vertical, avg_height, avg_weight):
    vert_years = np.arange(2001,2019)
    height_weight_years = np.arange(1945,2019)
    fig, axis = plt.subplots(1,3)
    axis[0].plot(vert_years, avg_vertical)
    axis[0].grid(True)

    axis[1].plot(height_weight_years, avg_height)
    axis[1].grid(True)

    axis[2].plot(height_weight_years, avg_weight)
    axis[2].grid(True)

    plt.show()



f = open(r'C:\Users\jakel\NBA Historical Analysis\player_data.json','r')
player_data = json.load(f)
vertical_by_year = vertical_by_year(player_data)
height_weight_by_year = height_weight_by_year(player_data)
avg_verticals = plot_vertical_by_year(vertical_by_year)
avg_heights, avg_weights = plot_height_weight_by_year(height_weight_by_year)

plot_all(avg_verticals, avg_heights, avg_weights)


