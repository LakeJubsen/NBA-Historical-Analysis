# NBA-Historical-Analysis

My motivation for starting this project stemmed from a curiosity about how NBA basketball has evolved since the league started in 1946. Over the years,
the technical and physical skills of players have increased substantially as a result of the NBA's growing popularity and financial prosperity. 

I wanted to see how things like average player height, weight, vertical and other physical attributes has changed over time. The database attached (basketball.sqlite) has combine information on nearly every athlete since the 80's (although the data gets sparse as you go farther back in time). Additionally, I want to explore how the flow and style of games has evolved over time (points in the paint vs 3s vs mid range jumpers, points per minute, assists per minute, points per game).

I gained experience in the following areas while working on this project:
    [Reading data from SQLite database]
    [Creating and reading from large nested dictionaries using loops]
    [Plotting large datasets]
    [Handling errors in the case of missing data points]
    [Structuring my code in a logical manner using OOP]
    [Writing data to JSON file]
    [Reading data from JSON file]
    
There are four python files attached
    [collect_biometric_db_data.py: Reads relevant data from sqlite database, organizes it, and puts it into a json file]
    [analyze_biometric_data.py: Reads data from player_data.json and outputs graphs of how height, weight and vertical have changed over time]
    [collect_game_db_data.py: Reads shot data from each game in NBA history from sqlite database, organizes it, and puts it into game_data.json]
    [analyze_game_data.py: Reads data from game_data.json and outputs graphs of shot selection correlates to win percentage]
    
NOTE: Due to large size of full basketball.sqlite database, I was unable to save it to GitHub. To get output graphs, just run analyze_biometric_data.py or analyze_game_data.py.
    
