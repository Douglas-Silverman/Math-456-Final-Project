import csv

import pandas as pd

def create_struct(file_name) :
    data_struct = [] # [V Team, V ML, H Team, H ML, Winner name, V score, H score]
                     #    0       1      2      3        4          5        6
    data = pd.read_csv(file_name)

    indexNames = data[ pd.isnull(data['Team']) ].index
    data.drop(indexNames , inplace=True)

    for index, row in data.iterrows():
        if(index % 2 == 0) :
            if(type(row['ML']) == type("string")):
                row['ML'] = row['Close']
            data_struct.append([ row['Team'], row['ML'], -1, -1, row['Final'], row['Final'], -1])
        else :
            if(type(row['ML']) == type("string")):
                row['ML'] = row['Close']
            data_struct[len(data_struct) - 1][2] = row['Team']
            data_struct[len(data_struct) - 1][3] = row['ML']
            data_struct[len(data_struct) - 1][6] = row['Final']
            if(data_struct[len(data_struct) - 1][4] > row['Final']) :
                data_struct[len(data_struct) - 1][4] = data_struct[len(data_struct) - 1][0]
            elif(data_struct[len(data_struct) - 1][4] == row['Final']) :
                data_struct[len(data_struct) - 1][4] = 'Tie'
            else :
                data_struct[len(data_struct) - 1][4] = data_struct[len(data_struct) - 1][2]

    return data_struct

def team_stats(file_name) :
    # game[0] or game[2] is a string key in the team_struct dict
    team_struct = {} # [A attack, A defense, H attack, H defense, # A games, # H games]
                     #      0          1        2          3           4          5
    games = create_struct(file_name)
    total_home = 0
    total_away = 0
    for game in games:
        # if Visiting team not yet in dictionary, initialize it
        if(game[0] not in team_struct):
            team_struct[game[0]] = [0, 0, 0, 0, 0, 0] #initialize all the scores as 0
        # if Home team not yet in dictionary, initialize it
        if(game[2] not in team_struct):
            team_struct[game[2]] = [0, 0, 0, 0, 0, 0]
        
        V_team = team_struct[game[0]]
        H_team = team_struct[game[2]]
        # increment number of home and away games played for each team
        V_team[4] += 1
        H_team[5] += 1
        visitor_score = game[5] # visiting team's final score
        home_score = game[6]    # Home team's final score
        
        #visiting_score calcs
        total_away += visitor_score
        V_team[0] += visitor_score # increase A attack for visiting team
        H_team[3] += visitor_score # increase H defense for home team

        # home_score calcs
        total_home += home_score
        H_team[2] += home_score # increase H attack for home team
        V_team[1] += home_score # increase A defense for visiting team

    team_struct['total_away'] = total_away
    team_struct['total_home'] = total_home
    return team_struct