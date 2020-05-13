import csv

import pandas as pd

def create_struct(file_name) :
    data_struct = [] # [V Team, V ML, H Team, H ML, Winner name, V score, H score, Date]
                     #    0       1      2      3        4          5        6       7
    data = pd.read_csv(file_name)

    indexNames = data[ pd.isnull(data['Team']) ].index
    data.drop(indexNames , inplace=True)

    for index, row in data.iterrows():
        if(index % 2 == 0) :
            if(type(row['ML']) == type("string")):
                row['ML'] = row['Close']
            month = row['Date'] // 100
            # if(row['Date'] // 1000 == 0):
            #     month = row['Date'] // 100
            # else:
            #     month = row['Date'][0] + row['Date'][1]
            data_struct.append([ row['Team'], row['ML'], -1, -1, row['Final'], row['Final'], -1, month])
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

def team_stats(games) :
    # game[0] or game[2] is a string key in the team_struct dict
    team_struct = {} # [A attack, A defense, H attack, H defense, # A games, # H games]
                     #      0          1        2          3           4          5
    total_home = 0
    total_away = 0
    for game in games:
        # if Visiting team not yet in dictionary, initialize it
        if(game[0] not in team_struct):
            team_struct[game[0]] = [0, 0, 0, 0, 1, 1] #initialize all the scores as 0
        # if Home team not yet in dictionary, initialize it
        if(game[2] not in team_struct):
            team_struct[game[2]] = [0, 0, 0, 0, 1, 1]
        
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

def team_stats_per_month(prev_year, games):
    start_month = games[0][7]
    month_stats = {} # [teamstats for jan, team stats for feb, ...]
    curr_month = start_month
    month_games = []
    if('LOS' in prev_year):
        prev_year['LAD'] = prev_year['LOS']
    # splits the games into months
    # after getting all the games for a month, get the team_stats 
    for game in games:
        if(game[7] == curr_month):
            month_games.append(game)
        else:
            month_stats[curr_month] = team_stats(month_games)
            # increment curr_month
            curr_month = (curr_month + 1) % 12 # mod 12 since if we go from dec to jan we dont want 13 we want 1
            if(curr_month == 0) : # if month is december then it should be 12 not 0
                curr_month = 12
            month_games = []
            month_games.append(game)
    month_stats_copy = month_stats
    for month in month_stats:
        if(month != start_month):
            prev_month = month - 1
            if(prev_month == 0):
                prev_month = 12
            for team in month_stats[month]:
                if(team != 'total_home' and team != 'total_away'):
                    for i in range(0, len(month_stats[month][team])):
                        month_stats_copy[month][team][i] += month_stats[prev_month][team][i]
                else:
                    month_stats_copy[month][team] += month_stats[prev_month][team]
        elif(prev_year != 'no prev'):
            for team in month_stats[month]:
                if(team != 'total_home' and team != 'total_away'):
                    for i in range(0, len(month_stats[month][team])):
                        month_stats_copy[month][team][i] += prev_year[team][i]
                else:
                    month_stats_copy[month][team] += prev_year[team]
    return month_stats_copy
