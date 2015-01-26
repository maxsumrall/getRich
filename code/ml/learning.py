from ffnet import mlgraph, ffnet
from sklearn import linear_model
import networkx as NX
import math
import pylab
import csv
from datetime import *
import pymongo

client = pymongo.MongoClient('giedomak.nl')
db = client.test_database
results = db.results
print results

def converString(x):
    return float(x)

data = []

#how many days in the past has to be learned
learnDaysBack = 7
#on how many days has the neural network to be tested
learnData = -7
networkFormation = (learnDaysBack*9,20,10,1);
clf = linear_model.Lasso(alpha=0.1)

def convert_keys_to_string(dictionary):
    """Recursively converts dictionary keys to strings."""
    if not isinstance(dictionary, dict):
        return dictionary
    return dict((str(k).replace("\'", "\""), convert_keys_to_string(v))
        for k, v in dictionary.items())

def readData():
    #read data
    # with open('../../data/sentiSorted.csv', 'rb') as csvfile:
    #     rawData = csv.reader(csvfile, delimiter=';')
    #     rawData.next()
    #     for row in rawData:
    #         data.append(row[1:])
    # Read from mongodb
    lastStock = 0
    lastPrepared = [1/8, 1/8, 1/8, 1/8, 1/8, 1/8, 1/8, 1/8, 1]
    for i in range(0, 61):
        date = (datetime(2014, 8, 2) + timedelta(days=i))
        date_key = str(date.day) + "/" + str(date.month) + "/" + str(date.year)
        try:
            find = convert_keys_to_string(results.find({'x':date_key}).next())
            prepared = date_key, [find['joy'], find['trust'], find['fear'], find['surprise'], find['sadness'], find['disgust'],
                find['anger'], find['anticipation'], find['Stock']]
            if prepared[1][8] == 0:
                prepared[1][8] = lastStock
            lastStock = prepared[1][8]
            lastPrepared = prepared[1]

            data.append(prepared)
            print str(i) + " Yes"
            #data[-1]['x'] = str(data[-1]['x'])
            # del data[date_key]["_id"]
        except:
            prepared = date_key, lastPrepared
            data.append(prepared)
            print str(i) + " NOPE"


    #convert data so it can be pushed in to the neural network
    trainingSetInput = []
    trainingSetResult = []
    datesResult = []
    for i in range(learnDaysBack, len(data)+learnData):
        inputSet = []
        for j in range(0, learnDaysBack):
            inputSet.extend(data[i-learnDaysBack+j][1])
        trainingSetInput.append(map(converString, inputSet))
        trainingSetResult.append([converString(data[i][1][-1])])
        datesResult.append(data[i][0])

    maxValue = 0
    minValue = 1000000000
    differenceSum = 0
    maxDifference = 0

    for value in trainingSetResult:
        maxValue = max(value[0], maxValue)
        minValue = min(value[0], minValue)

    for i in range(1, len(trainingSetResult)):
        difference = abs(trainingSetResult[i][0]/trainingSetResult[i-1][0]-1)
        differenceSum = differenceSum + difference
        maxDifference = max(differenceSum, maxDifference)

    print "Raw data information = Difference absolute: " + str(maxValue-minValue) + " | difference percentage: " + str(abs(maxValue/minValue - 1))
    print "Raw average Average difference: " + str(differenceSum/(len(trainingSetResult)-1)) + " | maximal difference percentage: " + str(maxDifference)

    return trainingSetInput, trainingSetResult, datesResult

def testDatafunc(learnfunc, func, testDataInput, testDataActual, testDataActualDates):
    #test the neural network
    summationDifference = 0
    summationCount = 0
    maxDifference = 0

    for i in range(7, len(testDataInput)):
        learnInput = testDataInput[0:i]
        learnActual = testDataActual[0:i]
        learnfunc(learnInput, learnActual)
        result = func(testDataInput[i])
        difference = abs(testDataActual[i]/result - 1)
        print str(i) + " " + testDataActualDates[i] + ": actual: " + str(testDataActual[i]) + " | NN: " + str(result) + " | difference percentage: " + str(difference)
        summationCount += 1
        summationDifference += abs(testDataActual[i]/result - 1)
        maxDifference = max(difference, maxDifference)

    print "Average difference: " + str(summationDifference/summationCount) + " | maximal difference percentage: " + str(maxDifference)


trainingSetInput, trainingSetResult, trainingSetResultDates = readData()
testDataInput = trainingSetInput[learnData:]
testDataActual = trainingSetResult[learnData:]

#create and train neural network

'''print "Genetic"
conec = mlgraph(networkFormation)
net = ffnet(conec)
testDatafunc(net.train_genetic, net.call, trainingSetInput, trainingSetResult, trainingSetResultDates)

print "bfgs"
conec = mlgraph(networkFormation)
net = ffnet(conec)
testDatafunc(net.train_bfgs, net.call, trainingSetInput, trainingSetResult, trainingSetResultDates)

print "cg"
conec = mlgraph(networkFormation)
net = ffnet(conec)
testDatafunc(net.train_cg, net.call, trainingSetInput, trainingSetResult, trainingSetResultDates)

print "momentum"
conec = mlgraph(networkFormation)
net = ffnet(conec)
testDatafunc(net.train_momentum, net.call, trainingSetInput, trainingSetResult, trainingSetResultDates)

print "rprop"
conec = mlgraph(networkFormation)
net = ffnet(conec)
testDatafunc(net.train_rprop, net.call, trainingSetInput, trainingSetResult, trainingSetResultDates)

print "tnc"
conec = mlgraph(networkFormation)
net = ffnet(conec)
testDatafunc(net.train_tnc, net.call, trainingSetInput, trainingSetResult, trainingSetResultDates)'''

print "Lasso Bitches!"
testDatafunc(clf.fit, clf.predict, trainingSetInput, trainingSetResult, trainingSetResultDates)

#NX.draw(net.graph)
#pylab.show()
