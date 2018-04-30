# NBA Game Predictor
# File: predictor.py
# Authors: Tarmily Wen & Andrew Petrosky
#
# The main predictor function, which calls the
# the requested model to make the prediction

from src.vectors import get_vector
import src.predictors.baseline as baseline


def predict(date, home, away, predictor):
    v = get_vector(date, home, away, predictor)
    if predictor == "baseline":
        result = baseline.predict(v)
        if result:
            print("Home team (" + home + ") wins.")
        else:
            print("Away team (" + away + ") wins.")
    else:
        print("Not an implemented predictor.")
