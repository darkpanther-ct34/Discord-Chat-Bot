import json
import numpy as np
import torch
from model import NeuralNet
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from nltkFunc import tokenize, stem, bagofwords

"""
Extra training format
{
      "tag": "",
      "patterns": [],
      "responses": [
        
      ]
    }
"""


with open('data.json', 'r') as f:
    intents = json.load(f)

allWords = []
tags = []
xy = []
for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        w = tokenize(pattern)
        allWords.extend(w)
        xy.append((w, tag))

ignoreWords = ['?', '!', '.', ',']
allWords = [stem(w) for w in allWords if w not in ignoreWords]
allWords = sorted(set(allWords))
tags = sorted(set(tags))

x_train = []
y_train = []

for (patternSentance, tag) in xy:
    bag = bagofwords(patternSentance, allWords)
    x_train.append(bag)

    label = tags.index(tag)
    y_train.append(label)

x_train = np.array(x_train)
y_train = np.array(y_train)


class ChatDataset(Dataset):
    def __init__(self):
        self.nSamples = len(x_train)
        self.x_data = x_train
        self.y_data = y_train

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.nSamples


batch_size = 8
hiddenSize = 8
outputSize = len(tags)
inputSize = len(x_train[0])
learningRate = 0.001
numEpochs = 1000


dataset = ChatDataset()
trainLoader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True)


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNet(inputSize, hiddenSize, outputSize).to(device)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learningRate)


for epoch in range(numEpochs):
    for (words, labels) in trainLoader:
        words = words.to(device)
        labels = labels.to(device)
        labels = labels.type(torch.LongTensor)
        outputs = model(words)
        loss = criterion(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if (epoch + 1) % 100 == 0:
        print(f'epoch {epoch+1}/{numEpochs}, loss={loss.item():.4f}')


print(f'final loss, loss={loss.item():.4f}')


data = {
    "modelState": model.state_dict(),
    "inputSize": inputSize,
    "outputSize": outputSize,
    "hiddenSize": hiddenSize,
    "allWords": allWords,
    "tags": tags

}

FILE = "data.pth"
torch.save(data, FILE)

print(f'training complete. file saved to {FILE}')
