#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 18:11:07 2019
@proyect Oreilly Neural Networks
@section Introduction to python
@author: Gabriel Toro Retivoff
"""


import pandas as pd
import torch
import numpy as np

dataset = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data',
                      names=['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species'])

dataset['species'] = pd.Categorical(dataset['species']).codes

dataset = dataset.sample(frac=1, random_state=1234)

train_input = dataset.values[:120, :4]
train_target = dataset.values[:120, 4]

test_input = dataset.values[120:, :4]
test_target = dataset.values[120:, 4]

torch.manual_seed(1234)

hidden_units = 5

net = torch.nn.Sequential(
 torch.nn.Linear(4, hidden_units),
 torch.nn.ReLU(),
 torch.nn.Linear(hidden_units, 3)
)

criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(net.parameters(), lr=0.1, momentum=0.9)

# train
epochs = 100

for epoch in range(epochs):
 inputs = torch.autograd.Variable(torch.Tensor(train_input).float())
 targets = torch.autograd.Variable(torch.Tensor(train_target).long())

 optimizer.zero_grad()
 out = net(inputs)
 loss = criterion(out, targets)
 loss.backward()
 optimizer.step()

 if epoch == 0 or (epoch + 1) % 10 == 0:
     print('Epoch %d Loss: %.4f' % (epoch + 1, loss.item()))
     
inputs = torch.autograd.Variable(torch.Tensor(test_input).float())
targets = torch.autograd.Variable(torch.Tensor(test_target).long())

optimizer.zero_grad()
out = net(inputs)
_, predicted = torch.max(out.data, 1)

error_count = test_target.size - np.count_nonzero((targets == predicted).numpy())
print('Errors: %d; Accuracy: %d%%' % (error_count, 100 * torch.sum(targets == predicted) / test_target.size))