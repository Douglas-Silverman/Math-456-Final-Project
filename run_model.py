import pandas as pd
import math
from game_reader import *
import decimal

def calculate_winnings(file_name, winners, segments) :
    data = create_struct(file_name)
    initial_capitol = 1000
    max_bet_per_game = 1000 / len(data)
    bet_size = max_bet_per_game
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
        curr_profit = -1 * bet_size
        if(game[1] > game[3]) :
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

def payout(ML, bet_size) :
    if(ML < 0) :
        ml = -1 * ML
        return (bet_size) * ((100 / ml) + 1)
    return (bet_size)*((ML / 100) + 1)


def kelly_criterion(file_name, winners, segments) :
    data = create_struct(file_name)
    capital = 1000
    initial_bet_size = 0
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
        capital += profit
        if(capital < 0) :
            profit = -1000
            capital = -1
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

def martingale_model(file_name, winners, segments) :
    data = create_struct(file_name)
    initial_capitol = 1000
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
        if(not winners):
            if(game[1] > game[3]) :
                bet_team = game[0]
                bet_ML = game[1]
            else :
                bet_team = game[2]
                bet_ML = game[3]
        else : # winners
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

def oscars_grind(file_name, winners, segments) :
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
        if(not winners):
            if(game[1] > game[3]) :
                bet_team = game[0]
                bet_ML = game[1]
            else :
                bet_team = game[2]
                bet_ML = game[3]
        else : # winners
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

def poisson_model(file_name, winners, segments):
    game_data = create_struct(file_name)
    team_data = team_stats(file_name)
    profit = 0
    result = [] # filled with tuples for every 10% of games
    percent = len(game_data) // segments
    count = 1
    cutoff = (count * percent) - 1
    result.append([0, profit])
    index = 0
    for game in game_data :
        bet_team = ''
        bet_ML = 100
        bet_size = 5
        
        V_Team_Prob = poisson_prob_away(team_data, game, len(game_data))
        H_Team_Prob = poisson_prob_home(team_data, game, len(game_data))
        if(V_Team_Prob > H_Team_Prob):
            bet_team = game[0]
            bet_ML = game[1]
            bet_size = 5 + 10 * V_Team_Prob
        else:
            bet_team = game[2]
            bet_ML = game[3]
            bet_size = 5 + 10 * H_Team_Prob
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

def poisson(lambdaa, k):
    pmf = decimal.Decimal(0)
    pmf = ((lambdaa**k) * math.exp(-lambdaa)) / math.factorial(k)
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

    max_game_score = 40 # arbitrary max score
    if('BOS' in team_data):
        max_game_score = 15
    elif('Boston' in team_data):
        max_game_score = 140
    #Calculate probablility that Home wins regardless of score (up to max game score in this case)
    home_prob_win = 0
    for i in range (1, max_game_score):
        for j in range(0,i):
            home_prob_win += poisson(H_likely_score, i) * poisson(A_likely_score,j)
    return home_prob_win

