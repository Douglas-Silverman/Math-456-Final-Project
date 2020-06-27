from game_reader import *
from model import *
from graph import *
from decimal import Decimal

def run_favorites():
    plotSport("NFL Favorites", "NFL", bet_on_favorites)
    plotSport("NBA Favorites", "NBA", bet_on_favorites)
    plotSport("MLB Favorites", "MLB", bet_on_favorites)

def run_martingale():
    plotSport("NFL Martingale", "NFL", martingale_model)
    plotSport("NBA Martingale", "NBA", martingale_model)
    plotSport("MLB Martingale", "MLB", martingale_model)

def run_oscar_grind():
    plotSport("NFL Oscar's Grind", "NFL", oscars_grind)
    plotSport("NBA Oscar's Grind", "NBA", oscars_grind)
    plotSport("MLB Oscar's Grind", "MLB", oscars_grind)

def run_kelly_criterion():
    plotSport("NFL Kelly Criterion", "NFL", kelly_criterion)
    plotSport("NBA Kelly Criterion", "NBA", kelly_criterion)
    plotSport("MLB Kelly Criterion", "MLB", kelly_criterion)

def run_poisson():
    plotSport("NFL Poisson", "NFL", poisson_model)
    plotSport("NBA Poisson", "NBA", poisson_model)
    plotSport("MLB Poisson", "MLB", poisson_model)

def run_poisson_martingale():
    plotSport("NFL Poisson Martingale", "NFL", poisson_model_martingale)
    plotSport("NBA Poisson Martingale", "NBA", poisson_model_martingale)
    plotSport("MLB Poisson Martingale", "MLB", poisson_model_martingale)

def main():
    run_favorites()
    run_martingale()
    # run_oscar_grind()
    # run_kelly_criterion()
    run_poisson()
    # run_poisson_martingale()

main()