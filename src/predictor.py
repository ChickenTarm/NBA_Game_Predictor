# NBA Game Predictor
# File: predictor.py
# Authors: Tarmily Wen & Andrew Petrosky
#
# The main predictor function, which calls the
# the requested model to make the prediction

import numpy as np
import src.predictors.baseline as baseline
import src.predictors.svm as svm
import src.predictors.naive_bayes as nb
import src.predictors.neural_nets as nn


def evaluate_model(p, train_x, train_y, test_x, test_y):
    print("Testing on training data...")
    correct = 0.0
    total = 0.0
    for i in range(np.size(train_x, 0)):
        x = [train_x[i]]
        y_g = train_y[i]
        y = p.predict(x)
        if y == y_g:
            correct += 1.0
        total += 1.0
    acc = correct / total
    print("Training Accuracy = " + str(acc))
    print("Testing on test data...")
    correct = 0.0
    total = 0.0
    for i in range(np.size(test_x, 0)):
        x = [test_x[i]]
        y_g = test_y[i]
        y = p.predict(x)
        if y == y_g:
            correct += 1.0
        total += 1.0
    acc = correct / total
    print("Testing Accuracy = " + str(acc))


def predictor(pred):
    seasons = ["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017"]
    if pred == "baseline":
        train_x, train_y = [], []
        for season in seasons:
            xs = np.load("../labels/" + season + "/" + season + "_win_pct_vectors.npy").tolist()
            ys = np.load("../labels/" + season + "/" + season + "_labels.npy").tolist()
            train_x += xs
            train_y += ys
        test_x = np.load("../labels/2018/2018_win_pct_vectors.npy").tolist()
        test_y = np.load("../labels/2018/2018_labels.npy").tolist()
        baseline.model(train_x, train_y, test_x, test_y)
    elif pred == "basic_svm":
        train_x, train_y = [], []
        for season in seasons:
            xs = np.load("../labels/" + season + "/" + season + "_win_pct_vectors.npy")
            xs = xs.tolist()
            ys = np.load("../labels/" + season + "/" + season + "_labels.npy").tolist()
            train_x += xs
            train_y += ys
        test_x = np.load("../labels/2018/2018_win_pct_vectors.npy")
        test_y = np.load("../labels/2018/2018_labels.npy")
        train_x = np.array(train_x)
        train_y = np.array(train_y)
        p = svm.model(train_x, train_y)
        evaluate_model(p, train_x, train_y, test_x, test_y)
    elif pred == "basic_nb":
        train_x, train_y = [], []
        for season in seasons:
            xs = np.load("../labels/" + season + "/" + season + "_record_vectors.npy").tolist()
            ys = np.load("../labels/" + season + "/" + season + "_labels.npy").tolist()
            train_x += xs
            train_y += ys
        test_x = np.load("../labels/2018/2018_record_vectors.npy")
        test_y = np.load("../labels/2018/2018_labels.npy")
        train_x = np.array(train_x)
        train_y = np.array(train_y)
        p = nb.model(train_x, train_y)
        evaluate_model(p, train_x, train_y, test_x, test_y)
    elif pred == "basic_nn":
        train_x, train_y = [], []
        for season in seasons:
            xs = np.load("../labels/" + season + "/" + season + "_record_vectors.npy").tolist()
            ys = np.load("../labels/" + season + "/" + season + "_labels.npy").tolist()
            train_x += xs
            train_y += ys
        test_x = np.load("../labels/2018/2018_record_vectors.npy")
        test_y = np.load("../labels/2018/2018_labels.npy")
        train_x = np.array(train_x)
        train_y = np.array(train_y)
        nn.model(train_x, train_y, test_x, test_y, "basic")

    elif pred == "advanced_svm":
        train_x, train_y = [], []
        for season in seasons:
            xs = np.load("../labels/" + season + "/" + season + "_rec_cum_stat_vectors.npy").tolist()
            ys = np.load("../labels/" + season + "/" + season + "_labels.npy").tolist()
            train_x += xs
            train_y += ys
        test_x = np.load("../labels/2018/2018_rec_cum_stat_vectors.npy")
        test_y = np.load("../labels/2018/2018_labels.npy")
        train_x = np.array(train_x)
        train_y = np.array(train_y)
        p = svm.model(train_x, train_y)
        evaluate_model(p, train_x, train_y, test_x, test_y)
    elif pred == "advanced_nb":
        train_x, train_y = [], []
        for season in seasons:
            xs = np.load("../labels/" + season + "/" + season + "_rec_cum_stat_vectors.npy").tolist()
            ys = np.load("../labels/" + season + "/" + season + "_labels.npy").tolist()
            train_x += xs
            train_y += ys
        test_x = np.load("../labels/2018/2018_rec_cum_stat_vectors.npy")
        test_y = np.load("../labels/2018/2018_labels.npy")
        train_x = np.array(train_x)
        train_y = np.array(train_y)
        p = nb.model(train_x, train_y)
        evaluate_model(p, train_x, train_y, test_x, test_y)
    elif pred == "advanced_nn":
        train_x, train_y = [], []
        for season in seasons:
            xs = np.load("../labels/" + season + "/" + season + "_rec_cum_stat_vectors.npy").tolist()
            ys = np.load("../labels/" + season + "/" + season + "_labels.npy").tolist()
            train_x += xs
            train_y += ys
        test_x = np.load("../labels/2018/2018_rec_cum_stat_vectors.npy")
        test_y = np.load("../labels/2018/2018_labels.npy")
        train_x = np.array(train_x)
        train_y = np.array(train_y)
        nn.model(train_x, train_y, test_x, test_y, "advanced")
    else:
        print("Not an implemented predictor.")


if __name__ == '__main__':
    # # Test the baseline predictor
    # print("\nTesting baseline predictor...")
    # predictor("baseline")
    # # Test the basic SVM predictor
    print("\nTesting basic SVM predictor...")
    predictor("basic_svm")
    # # Test the basic naive bayes predictor
    # print("\nTesting basic Naive Bayes predictor...")
    # predictor("basic_nb")
    # # Test the basic NN predictor
    # print("\nTesting basic Neural Net predictor...")
    # predictor("basic_nn")

    # Test the advanced SVM predictor
    print("\n\nTesting advanced SVM predictor...")
    predictor("advanced_svm")
    # Test the advanced naive bayes predictor
    print("\nTesting advanced Naive Bayes predictor...")
    predictor("advanced_nb")
    # Test the advanced NN predictor
    print("\nTesting advanced Neural Net predictor...")
    predictor("advanced_nn")
