# NBA-Historical-Analysis

My motivation for starting this project stemmed from a curiosity about how NBA basketball has evolved since the league started in 1946. Over the years,
the technical and physical skills of players have increased substantially as a result of the NBA's growing popularity and financial prosperity. 

I wanted to see how things like average player height, weight, vertical and other physical attributes has changed over time. The database attached (basketball.sqlite) has combine information on nearly every athlete since the 80's (although the data gets sparse as you go farther back in time). Additionally, I want to explore how the flow and style of games have evolved over time (points in the paint vs 3s vs mid range jumpers, points per minute, assists per minute, points per game).

I also wanted to expand my data science skill-set. I gained experience in the following areas while working on this project
    Reading data from SQLite database
    Creating and reading from large nested dicitionaries using loops
    Plotting large datasets
    Handling errors in the case of missing data points
    Structuring my code in a logical manner using OOP
    Writing data
    
There are two python files attached
    collect_db_data.py: Reads relevant data from sqlite database, organizes it, and puts it into a json file
    analyze_data.py: Reads data from JSON file and outputs graphs of how height, weight and vertical have changed over time
    
    
