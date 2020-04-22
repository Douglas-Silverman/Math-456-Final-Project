from game_reader import *
from run_model import *
from graph import *

# print(calculate_winnings("./nba odds/nba odds 2019-20.csv", 0))

# plotModel("Betting on Winners vs NBA", "Games", calculate_winnings("./nba odds/nba odds 2019-20.csv", 0))

# plotSport("NFL Favorites", "NFL", calculate_winnings)
# plotSport("NBA Favorites", "NBA", calculate_winnings)
# plotSport("MLB Favorites", "MLB", calculate_winnings)

plotSport("NFL Martingale", "NFL", martingale_model)
plotSport("NBA Martingale", "NBA", martingale_model)
plotSport("MLB Martingale", "MLB", martingale_model)

plotSport("NFL Oscar's Grind", "NFL", oscars_grind)
plotSport("NBA Oscar's Grind", "NBA", oscars_grind)
plotSport("MLB Oscar's Grind", "MLB", oscars_grind)

plotSport("NFL Kelly Criterion", "NFL", kelly_criterion)
plotSport("NBA Kelly Criterion", "NBA", kelly_criterion)
plotSport("MLB Kelly Criterion", "MLB", kelly_criterion)

# team_stats("./nfl odds/nfl odds 2018-19.csv")
# print(poisson_model("./nba odds/nba odds 2017-18.csv", True, 100))

plotSport("NFL Poisson", "NFL", poisson_model)
plotSport("NBA Poisson", "NBA", poisson_model)
plotSport("MLB Poisson", "MLB", poisson_model)
