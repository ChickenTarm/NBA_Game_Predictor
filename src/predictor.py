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
import src.predictors.knn as knn


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
    seasons = ["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018"]
    seasons = ["2015", "2016", "2017", "2018"]
    rm = [0, 3, 6, 8, 12, 13, 16, 21, 23, 26, 29, 31, 33, 36, 38, 39, 41, 44, 47]
    if pred == "baseline":
        train_x, train_y, test_x, test_y = [], [], [], []
        for season in seasons:
            xs = np.load("../labels/" + season + "/" + season + "_win_pct_vectors.npy").tolist()
            ys = np.load("../labels/" + season + "/" + season + "_labels.npy").tolist()
            if season == "2018":
                train_x += xs[-(len(xs)-300):-300]
                train_y += ys[-(len(xs)-300):-300]
                test_x += xs[-300:]
                test_y += ys[-300:]
            else:
                train_x += xs[-(len(xs)-300):]
                train_y += ys[-(len(xs)-300):]
        baseline.model(train_x, train_y, test_x, test_y)
    elif pred == "basic_svm":
        train_x, train_y, test_x, test_y = [], [], [], []
        for season in seasons:
            xs = np.load("../labels/" + season + "/" + season + "_record_vectors.npy")
            xs = xs.tolist()
            ys = np.load("../labels/" + season + "/" + season + "_labels.npy").tolist()
            if season == "2018":
                train_x += xs[-(len(xs) - 300):-300]
                train_y += ys[-(len(xs) - 300):-300]
                test_x += xs[-300:]
                test_y += ys[-300:]
            else:
                train_x += xs[-(len(xs) - 300):]
                train_y += ys[-(len(xs) - 300):]
        test_x = np.array(test_x)
        test_y = np.array(test_y)
        train_x = np.array(train_x)
        train_y = np.array(train_y)
        p = svm.model(train_x, train_y)
        evaluate_model(p, train_x, train_y, test_x, test_y)
    elif pred == "basic_knn":
        train_x, train_y, test_x, test_y = [], [], [], []
        for season in seasons:
            xs = np.load("../labels/" + season + "/" + season + "_record_vectors.npy")
            xs = xs.tolist()
            ys = np.load("../labels/" + season + "/" + season + "_labels.npy").tolist()
            if season == "2018":
                train_x += xs[-(len(xs) - 300):-300]
                train_y += ys[-(len(xs) - 300):-300]
                test_x += xs[-300:]
                test_y += ys[-300:]
            else:
                train_x += xs[-(len(xs) - 300):]
                train_y += ys[-(len(xs) - 300):]
        test_x = np.array(test_x)
        test_y = np.array(test_y)
        train_x = np.array(train_x)
        train_y = np.array(train_y)
        p = knn.model(train_x, train_y)
        evaluate_model(p, train_x, train_y, test_x, test_y)
    elif pred == "basic_nb":
        train_x, train_y, test_x, test_y = [], [], [], []
        for season in seasons:
            xs = np.load("../labels/" + season + "/" + season + "_record_vectors.npy").tolist()
            ys = np.load("../labels/" + season + "/" + season + "_labels.npy").tolist()
            if season == "2018":
                train_x += xs[-(len(xs) - 300):-300]
                train_y += ys[-(len(xs) - 300):-300]
                test_x += xs[-300:]
                test_y += ys[-300:]
            else:
                train_x += xs[-(len(xs) - 300):]
                train_y += ys[-(len(xs) - 300):]
        test_x = np.array(test_x)
        test_y = np.array(test_y)
        train_x = np.array(train_x)
        train_y = np.array(train_y)
        p = nb.model(train_x, train_y)
        evaluate_model(p, train_x, train_y, test_x, test_y)
    elif pred == "basic_nn":
        train_x, train_y, test_x, test_y = [], [], [], []
        for season in seasons:
            xs = np.load("../labels/" + season + "/" + season + "_record_vectors.npy").tolist()
            ys = np.load("../labels/" + season + "/" + season + "_labels.npy").tolist()
            if season == "2018":
                train_x += xs[-(len(xs) - 300):-300]
                train_y += ys[-(len(xs) - 300):-300]
                test_x += xs[-300:]
                test_y += ys[-300:]
            else:
                train_x += xs[-(len(xs) - 300):]
                train_y += ys[-(len(xs) - 300):]
        test_x = np.array(test_x)
        test_y = np.array(test_y)
        train_x = np.array(train_x)
        train_y = np.array(train_y)
        train_x = np.array(train_x)
        train_y = np.array(train_y)
        nn.model(train_x, train_y, test_x, test_y, "basic")

    elif pred == "advanced_svm":
        train_x, train_y, test_x, test_y = [], [], [], []
        for season in seasons:
            file = "../labels/" + season + "/" + season + "_streak_vectors.npy"
            files_lbls = "../labels/" + season + "/" + season + "_labels.npy"
            xs = np.load(file).tolist()
            ys = np.load(files_lbls).tolist()
            train_x += xs[-(len(xs) - 300):-300]
            train_y += ys[-(len(xs) - 300):-300]
            test_x += xs[-300:]
            test_y += ys[-300:]
        else:
            train_x += xs[-(len(xs) - 300):]
            train_y += ys[-(len(xs) - 300):]
        test_x = np.array(test_x)
        test_y = np.array(test_y)
        train_x = np.array(train_x)
        train_y = np.array(train_y)
        # for j in range(len(test_x)):
        #     x = test_x[j]
        #     cnt = 0
        #     for i in range(10):
        #         for k in rm:
        #             ind = 10 + k + (i * 52)
        #             del x[ind - cnt]
        #             cnt += 1
        #     test_x[j] = x
        train_x = np.array(train_x)
        train_y = np.array(train_y)
        p = svm.model(train_x, train_y)
        evaluate_model(p, train_x, train_y, test_x, test_y)
    elif pred == "advanced_knn":
        train_x, train_y, test_x, test_y = [], [], [], []
        for season in seasons:
            xs = np.load("../labels/" + season + "/" + season + "_streak_vectors.npy")
            xs = xs.tolist()
            ys = np.load("../labels/" + season + "/" + season + "_labels.npy").tolist()
            # for j in range(len(xs)):
            #     x = xs[j]
            #     x = x[:-1]
            #     xs[j] = x
            if season == "2018":
                train_x += xs[-(len(xs) - 300):-300]
                train_y += ys[-(len(xs) - 300):-300]
                test_x += xs[-300:]
                test_y += ys[-300:]
            else:
                train_x += xs[-(len(xs) - 300):]
                train_y += ys[-(len(xs) - 300):]
        test_x = np.array(test_x)
        test_y = np.array(test_y)
        train_x = np.array(train_x)
        train_y = np.array(train_y)
        p = knn.model(train_x, train_y)
        evaluate_model(p, train_x, train_y, test_x, test_y)
    elif pred == "advanced_nb":
        train_x, train_y, test_x, test_y = [], [], [], []
        for season in seasons:
            xs = np.load("../labels/" + season + "/" + season + "_streak_vectors.npy").tolist()
            ys = np.load("../labels/" + season + "/" + season + "_labels.npy").tolist()
            if season == "2018":
                train_x += xs[-(len(xs) - 300):-300]
                train_y += ys[-(len(xs) - 300):-300]
                test_x += xs[-300:]
                test_y += ys[-300:]
            else:
                train_x += xs[-(len(xs) - 300):]
                train_y += ys[-(len(xs) - 300):]
        test_x = np.array(test_x)
        test_y = np.array(test_y)
        train_x = np.array(train_x)
        train_y = np.array(train_y)
        train_x = np.array(train_x)
        train_y = np.array(train_y)
        p = nb.model(train_x, train_y)
        evaluate_model(p, train_x, train_y, test_x, test_y)
    elif pred == "advanced_nn":
        train_x, train_y, test_x, test_y = [], [], [], []
        for season in seasons:
            xs = np.load("../labels/" + season + "/" + season + "_streak_vectors.npy").tolist()
            ys = np.load("../labels/" + season + "/" + season + "_labels.npy").tolist()
            if season == "2018":
                train_x += xs[-(len(xs) - 300):-300]
                train_y += ys[-(len(xs) - 300):-300]
                test_x += xs[-300:]
                test_y += ys[-300:]
            else:
                train_x += xs[-(len(xs) - 300):]
                train_y += ys[-(len(xs) - 300):]
        test_x = np.array(test_x)
        test_y = np.array(test_y)
        train_x = np.array(train_x)
        train_y = np.array(train_y)
        train_x = np.array(train_x)
        train_y = np.array(train_y)
        nn.model(train_x, train_y, test_x, test_y, "advanced")
    else:
        print("Not an implemented predictor.")


if __name__ == '__main__':
    # # Clean vector files
    # seasons = ["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018"]
    # for season in seasons:
    #     file = "../labels/" + season + "/" + season + "_rec_cum_stat_vectors.npy"
    #     file_new = "../labels/" + season + "/" + season + "_rec_cum_stat_vectors_530.npy"
    #     xs = np.load(file).tolist()
    #     xs_new = []
    #     for x in xs:
    #         if len(x) != 10 and len(x) != 270:
    #             xs_new += [x]
    #     np.save(file_new, np.array(xs_new))
    # seasons = ["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018"]
    # for season in seasons:
    #     file = "../labels/" + season + "/" + season + "_rec_cum_stat_vectors.npy"
    #     labels = "../labels/" + season + "/" + season + "_labels.npy"
    #     file_new = "../labels/" + season + "/" + season + "_labels_530.npy"
    #     xs = np.load(file).tolist()
    #     ys = np.load(labels).tolist()
    #     ys_new = []
    #     for i in range(len(xs)):
    #         x = xs[i]
    #         y = ys[i]
    #         if len(x) != 10 and len(x) != 270:
    #             ys_new += [y]
    #     np.save(file_new, np.array(ys_new))

    # Test the baseline predictor
    print("\nTraining baseline predictor...")
    predictor("baseline")
    # Test the basic SVM predictor
    print("\n\nTraining basic SVM predictor...")
    predictor("basic_svm")
    # Test the basic KNN predictor
    print("\nTraining basic KNN predictor...")
    predictor("basic_knn")
    # Test the basic naive bayes predictor
    print("\nTraining basic Naive Bayes predictor...")
    predictor("basic_nb")
    # Test the basic NN predictor
    print("\nTraining basic Neural Net predictor...")
    predictor("basic_nn")

    # Test the advanced SVM predictor
    print("\n\nTraining advanced SVM predictor...")
    predictor("advanced_svm")
    # Test the advanced KNN predictor
    print("\nTraining advanced KNN predictor...")
    predictor("advanced_knn")
    # Test the advanced naive bayes predictor
    print("\nTraining advanced Naive Bayes predictor...")
    predictor("advanced_nb")
    # Test the advanced NN predictor
    print("\nTraining advanced Neural Net predictor...")
    predictor("advanced_nn")
