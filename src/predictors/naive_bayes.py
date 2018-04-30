# NBA Game Predictor
# File: naive_bayes.py
# Authors: Tarmily Wen & Andrew Petrosky
#
# A basic naives bayes predictor based only
# on the home and away team winning percentages

from sklearn.naive_bayes import GaussianNB


def model(train_x, train_y):
    clf = GaussianNB()
    clf.fit(train_x, train_y)
    return clf
