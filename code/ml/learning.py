from ffnet import mlgraph, ffnet
from sklearn import linear_model
import networkx as NX
import math
import pylab
import csv

def converString(x): return float(x)

data = []

#how many days in the past has to be learned
learnDaysBack = 14
#on how many days has the neural network to be tested
learnData = -14
networkFormation = (learnDaysBack*9,20,10,1);
clf = linear_model.Lasso(alpha=0.1)

def readData():
    #read data
    with open('/Users/max/Documents/getRich/data/sentiSorted.csv', 'rb') as csvfile:
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

    maxValue = 0
    minValue = 1000000000

    for value in trainingSetResult:
        maxValue = max(value[0], maxValue)
        minValue = min(value[0], minValue)

    print "Raw data information = Difference absolute: " + str(maxValue-minValue) + " | difference percentage: " + str(abs(maxValue/minValue - 1))

    return trainingSetInput, trainingSetResult

def testData(nn, testDataInput, testDataActual):
    #test the neural network
    summationDifference = 0
    summationCount = 0
    maxDifference = 0

    for i in range(0, len(testDataInput)):
        result = net.call(testDataInput[i])
        difference = abs(testDataActual[i]/result - 1)
        #print "actual: " + str(testDataActual[i]) + " | NN: " + str(result) + " | difference percentage: " + str(difference)
        summationCount += 1
        summationDifference += abs(testDataActual[i]/result - 1)
        maxDifference = max(difference, maxDifference)

    print "Average difference: " + str(summationDifference/summationCount) + " | maximal difference percentage: " + str(maxDifference)

trainingSetInput, trainingSetResult = readData()
testDataInput = trainingSetInput[learnData:]
testDataActual = trainingSetResult[learnData:]

#create and train neural network
print "Genetic"
conec = mlgraph(networkFormation)
net = ffnet(conec)
net.train_genetic(trainingSetInput[:learnData], trainingSetResult[:learnData])
testData(net, testDataInput, testDataActual)

print "bfgs"
conec = mlgraph(networkFormation)
net = ffnet(conec)
net.train_bfgs(trainingSetInput[:learnData], trainingSetResult[:learnData])
testData(net, testDataInput, testDataActual)

print "cg"
conec = mlgraph(networkFormation)
net = ffnet(conec)
net.train_cg(trainingSetInput[:learnData], trainingSetResult[:learnData])
testData(net, testDataInput, testDataActual)

print "momentum"
conec = mlgraph(networkFormation)
net = ffnet(conec)
net.train_momentum(trainingSetInput[:learnData], trainingSetResult[:learnData])
testData(net, testDataInput, testDataActual)

print "rprop"
conec = mlgraph(networkFormation)
net = ffnet(conec)
net.train_rprop(trainingSetInput[:learnData], trainingSetResult[:learnData])
testData(net, testDataInput, testDataActual)

print "tnc"
conec = mlgraph(networkFormation)
net = ffnet(conec)
net.train_tnc(trainingSetInput[:learnData], trainingSetResult[:learnData])
testData(net, testDataInput, testDataActual)

print "Lasso Bitches!"
clf.fit(trainingSetInput[:learnData], trainingSetResult[:learnData])
predicts = []
for each in zip(testDataInput, testDataActual):
    predicts.append(clf.predict(each[0]))
    #print "Actual: " + str(each[1]) + " Predict: " + str(predicted) + " Difference: " + str(math.fabs(each[1] - predicted))
    print str(each[1]).replace("[","").replace("]","")
print " ;;;"
for i in predicts:
    print str(i).replace("[","").replace("]","")
#NX.draw(net.graph)
#pylab.show()