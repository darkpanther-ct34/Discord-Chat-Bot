import torch
import torch.nn as nn


class NeuralNet(nn.Module):
    def __init__(self, inputsize, hiddensize, numclasses):
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(inputsize, hiddensize)
        self.l2 = nn.Linear(hiddensize, hiddensize)
        self.l3 = nn.Linear(hiddensize, inputsize)
        self.relu = nn.ReLU()

    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        return out
