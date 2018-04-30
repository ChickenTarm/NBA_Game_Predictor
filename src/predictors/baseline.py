# NBA Game Predictor
# File: baseline.py
# Authors: Tarmily Wen & Andrew Petrosky
#
# A baseline predictor based purely of winning percentage


def predict(v):
    home_win_pct = v[0]
    away_win_pct = v[1]
    if home_win_pct < away_win_pct:
        return 0
    else:
        return 1
