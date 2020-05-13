import pandas as pd
import math
from game_reader import *
from decimal import Decimal


###############################################################
# Func bet_on_favorites:
#
#   this model bets on the favorite in every game for an entire season
#   the bet size for each game is based on the number of games in the season
#
######### Parameters:
#
# | Parameter | Data Type | Description                            | Example                                        |
# | --------- | --------- | -------------------------------------- | ---------------------------------------------- |
# | file_name | string    | the name of the file to be run         | filename : "./nba odds/nba odds 2017-2018.csv" |
# | favorite  | boolean   | true if to bet on favorite(unused)     | favorite : True                                |
# | segments  | int       | number of segments (used for graphing) | segments : 100                                 |
#
######### Returns:
#
# An array of tuples (actually array of arrays). Each tuple stores the amount through the season and the current profit.
#
# | Key    | Data Type            | Description                                                           | Example                             |
# | ------ | -------------------- | --------------------------------------------------------------------- | ----------------------------------- |
# | result | [[int, float]]       | array of arrays that store the current progression and current profit | [[0,0], [17, 3.984], [34, -10.345]] |


def bet_on_favorites(file_name, favorites, segments) :
    data = create_struct(file_name) # array of games
    initial_capitol = 1000 
    max_bet_per_game = initial_capitol / len(data) 
    bet_size = max_bet_per_game
    profit = 0 
    result = [] # filled with tuples for every 1/segment
    percent = len(data) // segments # percent through the season
    count = 1 
    cutoff = (count * percent) - 1 
    result.append([0, profit])
    index = 0 # index represent the current index of game
    for game in data :
        bet_team = ''
        bet_ML = 100
        curr_profit = -1 * bet_size # once you make the bet you are at a deficit, if you win then you make profit
        # if the ML of team 0 is < the ML of 
        if(game[1] < game[3]) : 
            bet_team = game[0]
            bet_ML = game[1]
        else :
            bet_team = game[2]
            bet_ML = game[3]
        if(game[4] == bet_team) : # you won!
            curr_profit += payout(bet_ML, bet_size)
        profit += curr_profit
        if(index == cutoff and count < segments) :
            result.append([cutoff, profit])
            count += 1
            cutoff = (count * percent) - 1
        index += 1
    result.append([len(data) - 1, profit])
    return result

###############################################################
# Func payout:
#
#   this is a helper function that 

def payout(ML, bet_size) :
    if(ML < 0) :
        ml = -1 * ML
        return (bet_size) * ((100 / ml) + 1)
    return (bet_size)*((ML / 100) + 1)


###############################################################
# Func kelly_criterion:
#
#   this model bets on the favorite in every game for an entire season
#   the bet size for each game is based on the probability that the favorites win
#   example: if team A has a 70% chance of winning (determined by Money Line)
#            the bet size would be 40% of capitol
#
######### Parameters:
#
# | Parameter | Data Type | Description                            | Example                                        |
# | --------- | --------- | -------------------------------------- | ---------------------------------------------- |
# | file_name | string    | the name of the file to be run         | filename : "./nba odds/nba odds 2017-2018.csv" |
# | favorite  | boolean   | true if to bet on favorite(unused)     | favorite : True                                |
# | segments  | int       | number of segments (used for graphing) | segments : 100                                 |
#
######### Returns:
#
# An array of tuples (actually array of arrays). Each tuple stores the amount through the season and the current profit.
#
# | Key    | Data Type            | Description                                                           | Example                             |
# | ------ | -------------------- | --------------------------------------------------------------------- | ----------------------------------- |
# | result | [[int, float]]       | array of arrays that store the current progression and current profit | [[0,0], [17, 3.984], [34, -10.345]] |

def kelly_criterion(file_name, favorites, segments) :
    data = create_struct(file_name)
    capital = 1000
    profit = 0
    result = [] # filled with tuples for every 10% of games
    percent = len(data) // segments
    count = 1
    cutoff = (count * percent) - 1
    result.append([0, profit])
    index = 0
    for game in data :
        bet_team = ''
        bet_ML = 100
        if(game[1] < game[3]):
            bet_team = game[0]
            bet_ML = game[1]
        else:
            bet_team = game[2]
            bet_ML = game[3]
        bet_team_prob = get_prob(bet_ML)
        bet_size = ((bet_team_prob * 2) - 1) * capital
        curr_profit = -1 * bet_size
        if(game[4] == bet_team) : # you won!
            curr_profit += payout(bet_ML, bet_size)
        profit += curr_profit
        capital += curr_profit
        if(index == cutoff and count < segments) :
            result.append([cutoff, profit])
            count += 1
            cutoff = (count * percent) - 1
        index += 1
    result.append([len(data) - 1, profit])
    return result

def get_prob(ML) :
    if(ML < 0) :
        ml = -1 * ML
        return (ml / (ml + 100))
    else :
        return (100 / (ML + 100))

###############################################################
# Func martingale_model:
#
#   -this model bets on either the underdogs or the favorites in every game for an entire season
#   -the bet size for each game is based on profit rounds
#   -a profit round represnts the amount lost since the last won bet
#   -the bet size is increased so that if that bet is won, the payout will be make up the deficit
#   -the initial bet size is determined so that ~10 lost bets in a row will result in bankruptcy
#
######### Parameters:
#
# | Parameter | Data Type | Description                            | Example                                        |
# | --------- | --------- | -------------------------------------- | ---------------------------------------------- |
# | file_name | string    | the name of the file to be run         | filename : "./nba odds/nba odds 2017-2018.csv" |
# | favorite  | boolean   | true if to bet on favorite             | favorite : True                                |
# | segments  | int       | number of segments (used for graphing) | segments : 100                                 |
#
######### Returns:
#
# An array of tuples (actually array of arrays). Each tuple stores the amount through the season and the current profit.
#
# | Key    | Data Type            | Description                                                           | Example                             |
# | ------ | -------------------- | --------------------------------------------------------------------- | ----------------------------------- |
# | result | [[int, float]]       | array of arrays that store the current progression and current profit | [[0,0], [17, 3.984], [34, -10.345]] |


def martingale_model(file_name, favorites, segments) :
    data = create_struct(file_name)
    initial_bet_size = 2
    profit = 0
    profit_round = 0 #profit per round
    result = [] # filled with tuples for every 10% of games
    percent = len(data) // segments
    count = 1
    cutoff = (count * percent) - 1
    result.append([0, profit])
    index = 0
    for game in data :
        bet_team = ''
        bet_ML = 100
        if(not favorites):
            if(game[1] > game[3]) :
                bet_team = game[0]
                bet_ML = game[1]
            else :
                bet_team = game[2]
                bet_ML = game[3]
        else : # favorites
            if(game[1] < game[3]):
                bet_team = game[0]
                bet_ML = game[1]
            else:
                bet_team = game[2]
                bet_ML = game[3]
        bet_size = martingale(game[3], profit_round, initial_bet_size)
        curr_profit = -1 * bet_size
        profit_round += curr_profit
        if(game[4] == bet_team) : # you won!
            curr_profit += payout(bet_ML, bet_size)
            profit_round = 0
        profit += curr_profit
        if(index == cutoff and count < segments) :
            result.append([cutoff, profit])
            count += 1
            cutoff = (count * percent) - 1
        index += 1
    result.append([len(data) - 1, profit])
    return result


def martingale(ML, profit, initial_bet_size) :
    if(profit < 0 and profit > -0.1):
        profit = 0
    if(profit >= 0):
        return initial_bet_size
    else:
        ratio = payout(ML, 1) - 1
        return abs(profit) / ratio

###############################################################
# Func oscars_grind:
#
#   -this model bets on either the underdogs or the favorites in every game for an entire season
#   -the bet size for each game is based on profit rounds
#   -a profit round represnts the amount lost since the last won bet
#   -during a profit round, the bet size is increased by 1 after every win, this is analogous to hot streaks in blackjack
#   -the initial bet size is 1
#
######### Parameters:
#
# | Parameter | Data Type | Description                            | Example                                        |
# | --------- | --------- | -------------------------------------- | ---------------------------------------------- |
# | file_name | string    | the name of the file to be run         | filename : "./nba odds/nba odds 2017-2018.csv" |
# | favorite  | boolean   | true if to bet on favorite             | favorite : True                                |
# | segments  | int       | number of segments (used for graphing) | segments : 100                                 |
#
######### Returns:
#
# An array of tuples (actually array of arrays). Each tuple stores the amount through the season and the current profit.
#
# | Key    | Data Type            | Description                                                           | Example                             |
# | ------ | -------------------- | --------------------------------------------------------------------- | ----------------------------------- |
# | result | [[int, float]]       | array of arrays that store the current progression and current profit | [[0,0], [17, 3.984], [34, -10.345]] |

def oscars_grind(file_name, favorites, segments) :
    data = create_struct(file_name)
    initial_capitol = 1000
    initial_bet_size = 1
    next_bet_size = 1
    profit = 0
    profit_round = 0 #profit per round
    result = [] # filled with tuples for every 10% of games
    percent = len(data) // segments
    count = 1
    cutoff = (count * percent) - 1
    result.append([0, profit])
    index = 0
    for game in data :
        bet_team = ''
        bet_ML = 100
        if(not favorites):
            if(game[1] > game[3]) :
                bet_team = game[0]
                bet_ML = game[1]
            else :
                bet_team = game[2]
                bet_ML = game[3]
        else : # favorites
            if(game[1] < game[3]):
                bet_team = game[0]
                bet_ML = game[1]
            else:
                bet_team = game[2]
                bet_ML = game[3]
        bet_size = next_bet_size
        curr_profit = -1 * bet_size
        profit_round += curr_profit
        if(game[4] == bet_team) : # you won!
            curr_profit += payout(bet_ML, bet_size)
            profit_round += payout(bet_ML, bet_size)
            if(profit_round < 0) :
                next_bet_size += 1
            else :
                next_bet_size = 1
        profit += curr_profit
        if(index == cutoff and count < segments) :
            result.append([cutoff, profit])
            count += 1
            cutoff = (count * percent) - 1
        index += 1
    result.append([len(data) - 1, profit])
    return result


###############################################################
# Func poisson_model:
#
#   -this model "predicts" the winner of a game, bets on that team and records the profit or loss for every game in the season
#   -the way a prediction is made is by suming the probability that team A will beat team B with a score of X-Y for every possible X and Y
#    example: P(A scores 1 AND B scores 0) + P(A scores 2 AND B scores 0) + P(A scores 2 AND B scores 1) + P(A scores 3 AND B scores 0) + ... + P(A scores MAX_SCORE AND B scores MAX_SCORE - 1)
#   -Do this for team A winning every possible score and team B winning every possible score and the team with the higher prob of winning is the team you bet on
#   -bet size is 5 + 10 * probability of the chosen team winning (max bet = 15)
#
######### Parameters:
#
# | Parameter | Data Type | Description                            | Example                                        |
# | --------- | --------- | -------------------------------------- | ---------------------------------------------- |
# | file_name | string    | the name of the file to be run         | filename : "./nba odds/nba odds 2017-2018.csv" |
# | favorite  | boolean   | true if to bet on favorite(unused)     | favorite : True                                |
# | segments  | int       | number of segments (used for graphing) | segments : 100                                 |
#
######### Returns:
#
# An array of tuples (actually array of arrays). Each tuple stores the amount through the season and the current profit.
#
# | Key    | Data Type            | Description                                                           | Example                             |
# | ------ | -------------------- | --------------------------------------------------------------------- | ----------------------------------- |
# | result | [[int, float]]       | array of arrays that store the current progression and current profit | [[0,0], [17, 3.984], [34, -10.345]] |


def poisson_model(file_name, favorites, segments):
    game_data = create_struct(file_name)
    # this part of the function gets the file_name for the previous year of play
    prev_year = "no prev"
    if(file_name[23] != '7'):
        prev_year = file_name[0:23] + str(int(file_name[23]) - 1) + file_name[24:]
        if(file_name[2] == 'n'):
            if(file_name[26] == '0'):
                new_year = '19'
                prev_year = prev_year[0:25] + new_year + prev_year[27:]
            else:
                new_year = str(int(file_name[26]) - 1)
                prev_year = prev_year[0:26] + new_year + prev_year[27:]
        prev_year = team_stats(create_struct(prev_year))
    month_team_data = team_stats_per_month(prev_year, game_data) # obtains data for the previous year of play
    profit = 0
    result = [] # filled with tuples for every 10% of games
    percent = len(game_data) // segments
    count = 1
    cutoff = (count * percent) - 1
    result.append([0, profit])
    index = 0
    start_month = game_data[0][7]
    for game in game_data :
        if(game[7] != start_month):
            bet_team = ''
            bet_ML = 100
            bet_size = 5
            prev_month = game[7] - 1
            if(prev_month == 0):
                prev_month = 12
            V_Team_Prob = poisson_prob_away(month_team_data[prev_month], game, len(game_data))
            H_Team_Prob = poisson_prob_home(month_team_data[prev_month], game, len(game_data))
            if(V_Team_Prob > H_Team_Prob):
                bet_team = game[0]
                bet_ML = game[1]
                bet_size = 5 + 10 * float(V_Team_Prob)
            else:
                bet_team = game[2]
                bet_ML = game[3]
                bet_size = 5 + 10 * float(H_Team_Prob)
            curr_profit = -1 * bet_size
            if(game[4] == bet_team) : # you won!
                curr_profit += payout(bet_ML, bet_size)
            profit += curr_profit
        if(index == cutoff and count < segments) :
            result.append([cutoff, profit])
            count += 1
            cutoff = (count * percent) - 1
        index += 1
    result.append([len(game_data) - 1, profit])
    return result

def poissonNBA(lambdaa, k):
    pmf = Decimal(0)
    lambdaa = Decimal(lambdaa)
    k = Decimal(k)
    factorial = Decimal(0)
    if(k >= 50):
        factorial = Decimal(math.sqrt(Decimal(2*math.pi)*k)) * (Decimal(round(k/Decimal(math.e))))**k # stirling approx for factorial
    else:
        factorial = Decimal(math.factorial(k))
    pmf = ((lambdaa**k) * Decimal(math.exp( (Decimal(-1) *lambdaa)) )) / factorial
    return pmf

def poisson(lambdaa, k):
    pmf = 0
    factorial = math.factorial(k)
    pmf = ((lambdaa**k) * math.exp( (-1 *lambdaa) )) / factorial
    return pmf

# poisson prob that V team will win
def poisson_prob_away(team_data, game, number_of_games):
    Away_score = team_data['total_away']
    Home_score = team_data['total_home']
    season_away_attack = Away_score / number_of_games # Season's Away Attack Strength
    season_home_attack = Home_score / number_of_games # Season's Home Attack Strength

    # Conceded goals is just the two numbers in reverse
    season_away_defense = season_home_attack # Season's Away Defense Strength
    season_home_defense = season_away_attack # Season's Home Defense Strength

    home_stats = team_data[game[2]] # [A attack, A defense, H attack, H defense, # A games, # H games]
    away_stats = team_data[game[0]] #      0          1        2          3           4          5
    
    # HOME SCORE CALCULATIONS
    # Home team's attack strength = (home points scored / total home games) / Seaons's Home Attack Strength
    AttackH = (home_stats[2] / home_stats[5]) / season_home_attack

    # Away team's defense strength = (away goals conceded from home / total away games) / Season's Away Defense Strength
    DefenseA = (away_stats[1] / away_stats[4]) / season_away_defense

    # Home's likely score = Home's Attack * Defense's Defense * Season's Away Defense Strength
    H_likely_score = AttackH * DefenseA * season_away_defense

    # AWAY SCORE CALCULATIONS
    # Away team's attack strength = (Attack away goals scored / total away games) / Season's Away Attack Strength
    AttackA = (away_stats[0] / away_stats[4])/season_away_attack

    # Home team's defense strength = (home goals conceded / total home games) / Season's Home Defense Strength
    DefenseH = (home_stats[3] / home_stats[5]) / season_home_defense

    # Away's Likely score = Away's Attack * Homes's Defense * Season's Home Defense Strength
    A_likely_score = AttackA * DefenseH * season_home_defense
    initial_score = 0
    max_game_score = 40 # arbitrary max score
    if('BOS' in team_data):
        max_game_score = 15
    elif('Boston' in team_data):
        max_game_score = 140
        initial_score = 50
    #Calculate probablility that Home wins regardless of score (up to max game score in this case)
    away_prob_win = 0
    initial_score = 0
    max_game_score = 40 # arbitrary max score
    if('BOS' in team_data):
        max_game_score = 15
    elif('Boston' in team_data):
        max_game_score = 140
        initial_score = 50
        for i in range (initial_score + 1, max_game_score):
            for j in range(initial_score, i):
                away_prob_win += poissonNBA(A_likely_score, i) * poissonNBA(H_likely_score, j)
    else:
        for i in range (initial_score + 1, max_game_score):
            for j in range(initial_score, i):
                away_prob_win += poisson(A_likely_score, i) * poisson(H_likely_score, j)
    return away_prob_win


    # poisson prob that H team will win
def poisson_prob_home(team_data, game, number_of_games):
    Away_score = team_data['total_away']
    Home_score = team_data['total_home']
    season_away_attack = Away_score / number_of_games # Season's Away Attack Strength
    season_home_attack = Home_score / number_of_games # Season's Home Attack Strength

    # Conceded goals is just the two numbers in reverse
    season_away_defense = season_home_attack # Season's Away Defense Strength
    season_home_defense = season_away_attack # Season's Home Defense Strength

    home_stats = team_data[game[2]] # [A attack, A defense, H attack, H defense, # A games, # H games]
    away_stats = team_data[game[0]] #      0          1        2          3           4          5
    # HOME SCORE CALCULATIONS
    # Home team's attack strength = (home points scored / total home games) / Seaons's Home Attack Strength
    AttackH = (home_stats[2] / home_stats[5]) / season_home_attack

    # Away team's defense strength = (away goals conceded from home / total away games) / Season's Away Defense Strength
    DefenseA = (away_stats[1] / away_stats[4]) / season_away_defense

    # Home's likely score = Home's Attack * Defense's Defense * Season's Away Defense Strength
    H_likely_score = AttackH * DefenseA * season_away_defense

    # AWAY SCORE CALCULATIONS
    # Away team's attack strength = (Attack away goals scored / total away games) / Season's Away Attack Strength
    AttackA = (away_stats[0] / away_stats[4])/season_away_attack

    # Home team's defense strength = (home goals conceded / total home games) / Season's Home Defense Strength
    DefenseH = (home_stats[3] / home_stats[5]) / season_home_defense

    # Away's Likely score = Away's Attack * Homes's Defense * Season's Home Defense Strength
    A_likely_score = AttackA * DefenseH * season_home_defense
    
    # Calculate probablility that Home wins regardless of score (up to max game score in this case)
    home_prob_win = 0
    initial_score = 0
    max_game_score = 40 # arbitrary max score
    if('BOS' in team_data):
        max_game_score = 15
    elif('Boston' in team_data):
        initial_score = 50
        max_game_score = 140
        for i in range (initial_score + 1, max_game_score):
            for j in range(0,i):
                home_prob_win += poissonNBA(H_likely_score, i) * poissonNBA(A_likely_score, j)
    else:
        for i in range (initial_score + 1, max_game_score):
            for j in range(0,i):
                home_prob_win += poisson(H_likely_score, i) * poisson(A_likely_score, j)
    return home_prob_win

###############################################################
# Func poisson_model_martingale:
#
#   -this function works the same as poisson_model except the bet size is different
#   -the bet size is determined the same way as martingale_model, with profit rounds
#   -the initial bet size is 3
#
######### Parameters:
#
# | Parameter | Data Type | Description                            | Example                                        |
# | --------- | --------- | -------------------------------------- | ---------------------------------------------- |
# | file_name | string    | the name of the file to be run         | filename : "./nba odds/nba odds 2017-2018.csv" |
# | favorite  | boolean   | true if to bet on favorite(unused)     | favorite : True                                |
# | segments  | int       | number of segments (used for graphing) | segments : 100                                 |
#
######### Returns:
#
# An array of tuples (actually array of arrays). Each tuple stores the amount through the season and the current profit.
#
# | Key    | Data Type            | Description                                                           | Example                             |
# | ------ | -------------------- | --------------------------------------------------------------------- | ----------------------------------- |
# | result | [[int, float]]       | array of arrays that store the current progression and current profit | [[0,0], [17, 3.984], [34, -10.345]] |


def poisson_model_martingale(file_name, favorites, segments):
    game_data = create_struct(file_name)
    # team_data = team_stats(game_data)
    prev_year = "no prev"
    if(file_name[23] != '7'):
        prev_year = file_name[0:23] + str(int(file_name[23]) - 1) + file_name[24:]
        if(file_name[2] == 'n'):
            if(file_name[26] == '0'):
                new_year = '19'
                prev_year = prev_year[0:25] + new_year + prev_year[27:]
            else:
                new_year = str(int(file_name[26]) - 1)
                prev_year = prev_year[0:26] + new_year + prev_year[27:]
        prev_year = team_stats(create_struct(prev_year))
    month_team_data = team_stats_per_month(prev_year, game_data)
    profit = 0
    profit_round = 0
    initial_bet_size = 3
    result = [] # filled with tuples for every 10% of games
    percent = len(game_data) // segments
    count = 1
    cutoff = (count * percent) - 1
    result.append([0, profit])
    index = 0
    start_month = game_data[0][7]
    for game in game_data :
        if(game[7] != start_month):
            bet_team = ''
            bet_ML = 100
            bet_size = 5
            prev_month = game[7] - 1
            if(prev_month == 0):
                prev_month = 12
            V_Team_Prob = poisson_prob_away(month_team_data[prev_month], game, len(game_data))
            H_Team_Prob = poisson_prob_home(month_team_data[prev_month], game, len(game_data))
            if(V_Team_Prob > H_Team_Prob):
                bet_team = game[0]
                bet_ML = game[1]
            else:
                bet_team = game[2]
                bet_ML = game[3]
            bet_size = martingale(bet_ML, profit_round, initial_bet_size)
            curr_profit = -1 * bet_size
            profit_round += curr_profit
            if(game[4] == bet_team) : # you won!
                curr_profit += payout(bet_ML, bet_size)
                profit_round = 0
            profit += curr_profit
        if(index == cutoff and count < segments) :
            result.append([cutoff, profit])
            count += 1
            cutoff = (count * percent) - 1
        index += 1
    result.append([len(game_data) - 1, profit])
    return result


