# NBA Game Predictor
# File: knn.py
# Authors: Tarmily Wen & Andrew Petrosky
#
# An KNN classifier

from sklearn.neighbors import KNeighborsClassifier


def model(train_x, train_y):
    clf = KNeighborsClassifier(n_neighbors=300, weights="distance")
    clf.fit(train_x, train_y)
    return clf
