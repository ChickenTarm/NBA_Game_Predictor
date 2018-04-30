# NBA Game Predictor
# File: baseline.py
# Authors: Tarmily Wen & Andrew Petrosky
#
# A baseline predictor based purely of winning percentage


def model(train_x, train_y, test_x, test_y):
    # Train test
    print("Testing on training data...")
    correct = 0.0
    total = 0.0
    for i in range(len(train_x)):
        t = 0 if train_x[i][0] < train_x[i][1] else 1
        if t == train_y[i]:
            correct += 1.0
        total += 1.0
    acc = correct / total
    print("Training Accuracy = " + str(acc))
    print("Testing on test data...")
    correct = 0.0
    total = 0.0
    for i in range(len(test_x)):
        t = 0 if test_x[i][0] < test_x[i][1] else 1
        if t == test_y[i]:
            correct += 1.0
        total += 1.0
    acc = correct / total
    print("Testing Accuracy = " + str(acc))
