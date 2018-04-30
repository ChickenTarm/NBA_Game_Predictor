# NBA Game Predictor
# File: svm.py
# Authors: Tarmily Wen & Andrew Petrosky
#
# A basic SVM predictor based only on the home
# and away team winning percentages

from sklearn.svm import SVC


def model(train_x, train_y):
    clf = SVC(kernel='sigmoid')
    clf.fit(train_x, train_y)
    return clf
