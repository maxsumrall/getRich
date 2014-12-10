__author__ = 'michiel'
from ffnet import mlgraph, ffnet
import networkx as NX
import pylab
import csv

data = []

with open('..\\..\\..\\sentiSorted.csv', 'rb') as csvfile:
    rawData = csv.reader(csvfile, delimiter=';')
    rawData.next()
    for row in rawData:
        data.append(row[1:])

trainingSetInput = []
trainingSetResult = []
for i in range(7, len(data)-1):
    inputSet = []
    for j in range(0, 7):
        inputSet.extend(data[i-7+j])
    trainingSetInput.append(inputSet)
    trainingSetResult.append([data[i][-1]])

for dataLine in trainingSetResult:
    print dataLine

conec = mlgraph((63,40,20,1))
net = ffnet(conec)
#net.train_genetic()
#NX.draw_graphviz(net.graph, prog='dot')
#NX.draw(net.graph)
#pylab.show()