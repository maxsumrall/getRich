__author__ = 'michiel'
from ffnet import mlgraph, ffnet
import networkx as NX
import pylab
import csv

def converString(x): return float(x)

data = []

#how many days in the past has to be learned
learnDaysBack = 7
#on how many days has the neural network to be tested
learnData = -7

#read data
with open('..\\..\\data\\sentiSorted.csv', 'rb') as csvfile:
    rawData = csv.reader(csvfile, delimiter=';')
    rawData.next()
    for row in rawData:
        data.append(row[1:])

#convert data so it can be pushed in to the neural network
trainingSetInput = []
trainingSetResult = []
for i in range(learnDaysBack, len(data)+learnData):
    inputSet = []
    for j in range(0, learnDaysBack):
        inputSet.extend(data[i-learnDaysBack+j])
    trainingSetInput.append(map(converString, inputSet))
    trainingSetResult.append([converString(data[i][-1])])

#create and train neural network
conec = mlgraph((learnDaysBack*9,30,15,1))
net = ffnet(conec)
net.train_genetic(trainingSetInput[:learnData], trainingSetResult[:learnData])


#test the neural network
summationDifference = 0
summationCount = 0
maxDifference = 0

testDataInput = trainingSetInput[learnData:]
testDataActual = trainingSetResult[learnData:]
for i in range(0, len(testDataInput)):
    result = net.call(testDataInput[i])
    difference = abs(testDataActual[i]/result - 1)
    print "actual: " + str(testDataActual[i]) + " | NN: " + str(result) + " | difference: " + str(difference)
    summationCount += 1
    summationDifference += abs(testDataActual[i]/result - 1)
    maxDifference = max(difference, maxDifference)

print "Average difference: " + str(summationDifference/summationCount) + " | maximal difference: " + str(maxDifference)
#NX.draw(net.graph)
#pylab.show()