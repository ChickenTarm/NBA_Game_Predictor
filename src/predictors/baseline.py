# NBA Game Predictor
# File: baseline.py
# Authors: Tarmily Wen & Andrew Petrosky
#
# A baseline predictor based purely of winning percentage


def model():
    # Train test
    for season in ["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017"]:
        prefix = "../../data/" + season + "/"
        for game_file in os.listdir(prefix):
            game_file = os.fsdecode(game_file)[:-5]
            home_win_pct = v[0]
            away_win_pct = v[1]
            if home_win_pct < away_win_pct:
                return 0
            else:
                return 1
