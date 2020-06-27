import matplotlib.pyplot as plt
from model import * 
from game_reader import *


###############################################################
# func: plotSport
#
#   -this function runs the simulation and plots the results for a parameterized sport and model
#
######### Parameters:
#
# | Parameter | Data Type | Description                                          | Example                          |
# | --------- | --------- | ---------------------------------------------------- | -------------------------------- |
# | title     | string    | The title for the graph                              | title : "NFL Poisson Martingale" |
# | sport     | string    | Which sport should be simulated                      | sport : "NFL"                    |
# | function  | function  | The model used in the simulation (found in model.py) | function : poisson_martingale    |
#
######### Returns:
#
# nothing is returned

def plotSport(title, sport, function) :
    # load file names
    files = []
    if(sport == "NFL") :
        files.append("./nfl odds/nfl odds 2017-18.csv")
        files.append("./nfl odds/nfl odds 2018-19.csv")
        files.append("./nfl odds/nfl odds 2019-20.csv")
    if(sport == "NBA") :
        files.append("./nba odds/nba odds 2017-18.csv")
        files.append("./nba odds/nba odds 2018-19.csv")
        files.append("./nba odds/nba odds 2019-20.csv")
    if(sport == "MLB") :
        files.append("./mlb odds/mlb odds 2017.csv")
        files.append("./mlb odds/mlb odds 2018.csv")
        files.append("./mlb odds/mlb odds 2019.csv")
    
    count = 0 # keeps track of current season 
    yearPlot = plt.figure(figsize= ((6.4, 4.8))) # set figure size
    for year in files : 
        result = function(year, True, 100) # run simulation
        xVars = []
        scores = []
        # add data points to plot
        for currentTuple in result :
            xVars.append(currentTuple[0]) 
            scores.append(currentTuple[1])
        mark = "r"
        label = "2017 season"
        if(count == 1) :
            mark = "b"
            label = "2018 season"
        if(count == 2) :
            mark = "g"
            label = "2019 season"
        yearPlot = plt.plot(xVars, scores, mark, label = label) # plot the data points
        count = count + 1 # update year
    plt.xlabel("games") 
    plt.ylabel("profit")
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.show()