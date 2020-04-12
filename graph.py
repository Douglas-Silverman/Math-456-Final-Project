import matplotlib.pyplot as plt
from run_model import * 
from game_reader import *

def plotModel(title, xLabel, modelResult) :
    result = modelResult
    xVars = []
    scores = []
    
    for currentTuple in result :
        xVars.append(currentTuple[0])
        scores.append(currentTuple[1])
    
    print(xVars)
    print(scores)
    plt.plot(xVars, scores)
    plt.xlabel(xLabel)
    plt.ylabel("profit")
    plt.legend()
    plt.title(title)
    # scoreShort = []
    # for score in scores :
    #     scoreShort.append(round(score, 2))
    # for z in zip(xVars, scoreShort) :
    #     plt.annotate(("(%s, %s)"%z), xy = z, textcoords = "data") 
    plt.show()
    plt.clf()

def plotSport(title, sport) :
    files = []
    if(sport == "NFL") :
        files.append("./nfl odds/nfl odds 2017-2018.csv")
        files.append("./nfl odds/nfl odds 2018-2019.csv")
        files.append("./nfl odds/nfl odds 2019-2020.csv")
    if(sport == "NBA") :
        files.append("./nba odds/nba odds 2017-2018.csv")
        files.append("./nba odds/nba odds 2018-2019.csv")
        files.append("./nba odds/nba odds 2019-2020.csv")
    if(sport == "MLB") :
        files.append("./mlb odds/mlb odds 2017.csv")
        files.append("./mlb odds/mlb odds 2018.csv")
        files.append("./mlb odds/mlb odds 2019.csv")
    
    count = 0
    for year in files :
        result = calculate_winnings(year, 0)
        xVars = []
        scores = []
    
        for currentTuple in result :
            xVars.append(currentTuple[0])
            scores.append(currentTuple[1])

        mark = "ro"
        if(count == 1) :
            mark = "bx"
        if(count == 2) :
            mark == "g+"
        plt.plot(xVars, scores, mark)
        scoreShort = []
        for score in scores :
            scoreShort.append(round(score, 2))
        for z in zip(xVars, scoreShort) :
            plt.annotate(("(%s, %s)"%z), xy = z, textcoords = "data") 
        count += 1
    plt.xlabel("games")
    plt.ylabel("profit")
    plt.legend()
    plt.title(title)
    plt.show()