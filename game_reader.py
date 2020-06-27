import csv
import pandas as pd


# this function creates a data structure of all the games in the season. The data structure is a 2D array.
# The raw data is set up such that a game is represented by a pair of consecutive rows. Each row has the data
# for only 1 team of the contest. This function combines the pair of rows into a single data entry in the array.
# Once the whole csv file is parsed, the data structure is returned.
#
#   example:
#       data_struct[0] is in form [V Team, V ML, H Team, H ML, Winner name, V score, H score, Date]
#       data_struct[0][0] = V Team, data_struct[0][3] = H ML, data_struct[0][5] = V score, ... 
#



def create_struct(file_name) :
    data_struct = [] # [V Team, V ML, H Team, H ML, Winner name, V score, H score, Date]
                     #    0       1      2      3        4          5        6       7
    data = pd.read_csv(file_name)
    # drop all null values (this drops both data entries in a pair)
    indexNames = data[ pd.isnull(data['Team']) ].index
    data.drop(indexNames , inplace=True)

    # even indices indicate visting team data, odd indicies indicate home team data
    for index, row in data.iterrows(): 
        if(index % 2 == 0) :
            if(type(row['ML']) == type("string")): # cleans MLB data where row['ML'] = 'x' when the opening ML is not available
                row['ML'] = row['Close'] # use the closing ML instead
            month = row['Date'] // 100 # cleans the data (example: September = 900, December = 1200) 

            # initializes home team data as -1 to be filled out on next loop iteration
            data_struct.append([ row['Team'], row['ML'], -1, -1, row['Final'], row['Final'], -1, month]) 
        else :
            if(type(row['ML']) == type("string")): # cleans MLB data where row['ML'] = 'x' when the opening ML is not available
                row['ML'] = row['Close'] # use the closing ML instead
            
            # fill in home team data from last iteration
            data_struct[len(data_struct) - 1][2] = row['Team']
            data_struct[len(data_struct) - 1][3] = row['ML']
            data_struct[len(data_struct) - 1][6] = row['Final']

            # calculated winner or tie
            if(data_struct[len(data_struct) - 1][4] > row['Final']) :
                data_struct[len(data_struct) - 1][4] = data_struct[len(data_struct) - 1][0]
            elif(data_struct[len(data_struct) - 1][4] == row['Final']) :
                data_struct[len(data_struct) - 1][4] = 'Tie'
            else :
                data_struct[len(data_struct) - 1][4] = data_struct[len(data_struct) - 1][2]

    return data_struct

# This function creates a dictionary for every team in a given sport. It then fills the dictionary with the teams statistics
# for the inputed games. The games parameter usually contains a list of games played during a month. The returned dictionary
# has the data for every team that played during that month. 
#
# team_struct['NYY'] = [Away points scored, Away points given up, ...]
# team_struct['BOS'] = stats for boston red sox

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
        
        # visiting_score calcs
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

# this function returns an array of team_struct dictionaries for every month of play. So if I want the stats of the Yankees
# in September then that would be located in month_stats[9]['NYY']. Stats for the Boston Red Sox in October would be located
# at month_stats[10]['BOS']
#
# This function

######### Parameters:
#
# prev_year is the string of the file name for the previous year (example "./nfl odds/nfl odds 2017-18.csv")
# games is the array returned from the create_struct function

def team_stats_per_month(prev_year, games):
    start_month = games[0][7]
    month_stats = {} # [teamstats for jan, team stats for feb, ..., team stats for last month in season]
    curr_month = start_month
    month_games = []
    # cleans data where Los Angeles Dodgers are marked as LOS in 2017 but LAD in 2018 and 2019
    if('LOS' in prev_year):
        prev_year['LAD'] = prev_year['LOS']
    # splits the games into months
    # after getting all the games for a month, call team_stats and send those games
    for game in games:
        # add all games of curr_month to array
        if(game[7] == curr_month):
            month_games.append(game) 
        # once all the games are added
        else:
            month_stats[curr_month] = team_stats(month_games) # get the data for all the games added so far
            # increment curr_month
            curr_month = (curr_month + 1) % 12 # mod 12 since if we go from dec to jan we dont want 13 we want 1
            if(curr_month == 0) : # if month is december then it should be 12 not 0
                curr_month = 12
            month_games = [] # clear the games array
            month_games.append(game) # add the current game to the cleared array since its the first game of the next month
    month_stats_copy = month_stats
    # the next piece of code adds previous months data to current months data
    # for example all the stats for september get added to october, then all the stats for october get added to november
    # Now november has the stats for september through november instead of only the stats in november
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
