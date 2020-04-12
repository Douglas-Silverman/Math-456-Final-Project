import pandas as pd
from game_reader import create_struct

def calculate_winnings(file_name, model_name) :
    data = create_struct(file_name)
    initial_capitol = 1000
    max_bet_per_game = 1000 / len(data)
    bet_size = max_bet_per_game
    result = 0
    for game in data :
        bet_team = ''
        bet_ML = 100
        profit = -1 * bet_size
        if(game[1] > game[3]) :
            bet_team = game[0]
            bet_ML = game[1]
        else :
            bet_team = game[2]
            bet_ML = game[3]
        if(game[4] == bet_team) : # you won!
            profit += payout(bet_ML, bet_size)
        result += profit
    print(result)
    print(initial_capitol + result)

def payout(ML, bet_size) :
    if(ML < 0) :
        ml = -1 * ML
        return (bet_size) * ((100 / ml) + 1)
    return (bet_size)*((ML / 100) + 1)



def kelly_criterion(file_name, model_name) :
    data = create_struct(file_name)
    capitol = 1000
    bet_size = 0
    for game in data :
        bet_team = ''
        bet_ML = 100
        team1_Prob = get_prob(game[1])
        team2_Prob = get_prob(game[3])
        print(team1_Prob)
        if(team1_Prob > team2_Prob) :
            bet_team = game[0]
            bet_size = ((team1_Prob * 2) - 1) * capitol
            bet_ML = game[1]
        else :
            bet_team = game[2]
            bet_size = ((team2_Prob * 2) - 1) * capitol
            bet_ML = game[3]
        print(bet_size)
        profit = -1 * bet_size
        if(game[4] == bet_team) : # you won!
            profit += payout(bet_ML, bet_size)
        capitol += profit
        print(capitol)
    print(capitol)

def get_prob(ML) :
    if(ML < 0) :
        ml = -1 * ML
        return (ml / (ml + 100))
    else :
        return (100 / (ML + 100))