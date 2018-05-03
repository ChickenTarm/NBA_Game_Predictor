# NBA Game Predictor
# File: neural_nets.py
# Authors: Tarmily Wen & Andrew Petrosky
#
# Neural Nets trained on the given data

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torch.autograd import Variable


class NetA(nn.Module):
    def __init__(self):
        super(NetA, self).__init__()
        self.fc1 = nn.Linear(14, 10)
        self.relu = nn.ReLU()
        self.drop = nn.Dropout(0.3)
        self.fc2 = nn.Linear(10, 1000)
        self.prelu = nn.PReLU(1)
        self.fc3 = nn.Linear(1000, 500)
        self.fc4 = nn.Linear(500, 2)
        self.sig = nn.Sigmoid()

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.drop(out)
        out = self.fc2(out)
        out = self.prelu(out)
        out = self.fc3(out)
        out = self.drop(out)
        out = self.fc4(out)
        out = self.sig(out)
        return out


class NetB(nn.Module):
    def __init__(self):
        super(NetB, self).__init__()
        self.fc1 = nn.Linear(12, 10)
        self.relu = nn.ReLU()
        self.drop = nn.Dropout(0.3)
        self.fc2 = nn.Linear(10, 100)
        self.prelu = nn.PReLU(1)
        self.fc3 = nn.Linear(100, 50)
        self.fc4 = nn.Linear(50, 2)
        self.sig = nn.Sigmoid()

    def forward(self, x):
        out0 = self.fc1(x)
        out1 = self.relu(out0)
        out2 = self.drop(out1)
        out3 = self.fc2(out2)
        out4 = self.prelu(out3)
        out5 = self.fc3(out4)
        out6 = self.fc4(out5)
        out7 = self.sig(out6)
        return out7


# Train net
def train(net, loader, criterion, max_epochs, lr):
    optimizer = optim.Adam(net.parameters(), lr=lr)#, momentum=0.9)
    for epoch in range(max_epochs):
        for i, data in enumerate(loader, 0):
            # Get inputs and labels from data loader
            inputs, labels = data
            inputs, labels = Variable(inputs.float()), Variable(labels.long())
            # zero gradient
            optimizer.zero_grad()
            # Feed the input data into the network
            y_pred = net(inputs)
            # Calculate the loss using predicted labels and ground truth labels
            loss = criterion(y_pred, labels.long())#.view(len(labels), 1))
            # print(loss.data[0])
            # backpropogates to compute gradient
            loss.backward()
            # updates the weights
            optimizer.step()


# Test net
def test(net, test_loader, train_loader):
    # correct = 0
    # total = 0
    # for i, data in enumerate(train_loader, 0):
    #     # Get inputs and labels from data loader
    #     inputs, lbls = data
    #     inputs, labels = Variable(inputs.float()), Variable(lbls.long())
    #     # labels = labels.long
    #     # Feed the input data into the network
    #     y_pred = net(inputs)
    #     print(y_pred)
    #     # convert predicted labels into numpy
    #     pred_np = y_pred.data.numpy()
    #     # calculate the testing accuracy of the current model
    #     label_np = labels.data.numpy().reshape(len(labels), 1)
    #     for k in range(pred_np.shape[0]):
    #         p = np.argmax(pred_np[k, :])
    #         if p == label_np[k, :]:
    #             correct += 1
    #         total += 1
    # acc = float(correct) / float(total)
    # print("Training Accuracy = " + str(acc))

    correct = 0
    total = 0
    for i, data in enumerate(test_loader, 0):
        # Get inputs and labels from data loader
        inputs, lbls = data
        inputs, labels = Variable(inputs.float()), Variable(lbls.long())
        # labels = labels.long
        # Feed the input data into the network
        y_pred = net(inputs)
        # print(y_pred)
        # convert predicted labels into numpy
        pred_np = y_pred.data.numpy()
        # calculate the testing accuracy of the current model
        label_np = labels.data.numpy().reshape(len(labels), 1)
        for k in range(pred_np.shape[0]):
            p = np.argmax(pred_np[k, :])
            if p == label_np[k, :]:
                correct += 1
            total += 1
    acc = float(correct) / float(total)
    print("Testing Accuracy = " + str(acc))


def model(train_x, train_y, test_x, test_y, t):
    class DS(Dataset):
        def __init__(self):
            self.len = test_x.shape[0]
            self.x_data = torch.from_numpy(train_x)
            self.y_data = torch.from_numpy(train_y)

        def __len__(self):
            return self.len

        def __getitem__(self, idx):
            return self.x_data[idx], self.y_data[idx]

    class TestDataset(Dataset):
        def __init__(self):
            self.len = test_x.shape[0]
            self.x_data = torch.from_numpy(test_x)
            self.y_data = torch.from_numpy(test_y)

        def __len__(self):
            return self.len

        def __getitem__(self, idx):
            return self.x_data[idx], self.y_data[idx]

    net = NetA() if t == "advanced" else NetB()
    #net.train(False)
    bs = 123 if t == "basic" else 166

    # Specify the training data sets
    dataset = DS()
    train_loader = DataLoader(dataset=dataset, batch_size=bs)

    # Specify the testing data set
    testdataset = TestDataset()
    test_loader = DataLoader(dataset=testdataset, batch_size=bs)

    # Specify the parameters
    lr = 0.001
    max_epochs = 100
    criterion = nn.CrossEntropyLoss()

    train(net, train_loader, criterion, max_epochs, lr)
    test(net, test_loader, train_loader)
