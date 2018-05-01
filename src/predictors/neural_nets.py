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


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv1d(82, 128, 3)
        self.pool1 = nn.MaxPool1d(2)
        self.conv2 = nn.Conv1d(128, 256, 3)
        self.fc1 = nn.Linear(512, 600)
        self.fc2 = nn.Linear(600, 150)
        self.fc3 = nn.Linear(150, 82)

    def forward(self, x):
        x = x.unsqueeze(0)
        out = F.relu(self.conv1(x))
        out = self.pool1(out)
        out = F.relu(self.conv2(out))

        out = out.view(out.size(0), -1)
        out = F.relu(self.fc1(out))

        out = out.view(out.size(0), -1)
        out = F.relu(self.fc2(out))

        out = out.view(out.size(0), -1)
        out = F.relu(self.fc3(out))
        return out


# Train net
def train(net, loader, criterion, max_epochs, lr):
    optimizer = optim.SGD(net.parameters(), lr=lr, momentum=0.9)
    loss_np = np.zeros(max_epochs)
    accuracy = np.zeros(max_epochs)
    k = 0
    for epoch in range(max_epochs):
        acc = 0.0
        j = 0
        for i, data in enumerate(loader, 0):
            # Get inputs and labels from data loader
            inputs, labels = data
            inputs, labels = Variable(inputs), Variable(labels)
            labels = labels.long()
            # Feed the input data into the network
            y_pred = net(inputs)
            # Calculate the loss using predicted labels and ground truth labels
            loss = criterion(y_pred, labels[i])
            # zero gradient
            optimizer.zero_grad()
            # backpropogates to compute gradient
            loss.backward()
            # updates the weghts
            optimizer.step()
            # convert predicted laels into numpy
            pred_np = y_pred.data.numpy()
            # calculate the training accuracy of the current model
            label_np = labels.data.numpy().reshape(len(labels), 1)
            correct = 0
            total = 0
            for k in range(pred_np.shape[0]):
                p = np.argmax(pred_np[k, :])
                if p == label_np[k, :]:
                    correct += 1
                total += 1
            acc_i = float(correct) / float(total)
            acc = acc + acc_i
            j += 1

            loss_np[epoch] = loss.data.numpy()
        acc = acc / float(j)
        accuracy[epoch] = acc
    print("Training Accuracy = ", accuracy[k])


# Test net
def test(net, loader):
    correct = 0
    total = 0
    for i, data in enumerate(loader, 0):
        # Get inputs and labels from data loader
        inputs, labels = data
        inputs, labels = Variable(inputs), Variable(labels)
        labels = labels.long()
        # Feed the input data into the network
        y_pred = net(inputs)
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


def model(train_x, train_y, test_x, test_y):
    class DS(Dataset):
        def __init__(self):
            self.len = test_x.shape[0]
            self.x_data = torch.from_numpy(train_x).float()
            self.y_data = torch.from_numpy(train_y).float()

        def __len__(self):
            return self.len

        def __getitem__(self, idx):
            return self.x_data[idx], self.y_data[idx]

    class TestDataset(Dataset):
        def __init__(self):
            self.len = test_x.shape[0]
            self.x_data = torch.from_numpy(test_x).float()
            self.y_data = torch.from_numpy(test_y).float()

        def __len__(self):
            return self.len

        def __getitem__(self, idx):
            return self.x_data[idx], self.y_data[idx]

    net = Net()

    # Specify the training data sets
    dataset = DS()
    train_loader = DataLoader(dataset=dataset, batch_size=82)

    # Specify the testing data set
    testdataset = TestDataset()
    test_loader = DataLoader(dataset=testdataset, batch_size=82)

    # Specify the parameters
    lr = 0.001
    max_epochs = 1000
    criterion = nn.CrossEntropyLoss()

    train(net, train_loader, criterion, max_epochs, lr)
    test(net, test_loader)
