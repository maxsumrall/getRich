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
    print x
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
    for i in range(250):
        date = (datetime.today() + timedelta(days=-i))
        date_key = str(date.day) + "/" + str(date.month) + "/" + str(date.year)
        try:
            find = convert_keys_to_string(results.find({'x':date_key}).next())
            prepared = [ find['joy'],find['trust'],find['fear'],find['surprise'],find['sadness'],find['disgust'],
                find['anger'],find['anticipation'],find['Stock'] ]
            data.append( prepared )
            #data[-1]['x'] = str(data[-1]['x'])
            # del data[date_key]["_id"]
        except:
            pass

    print data


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

def testDatafunc(func, testDataInput, testDataActual):
    #test the neural network
    summationDifference = 0
    summationCount = 0
    maxDifference = 0

    for i in range(0, len(testDataInput)):
        result = func(testDataInput[i])
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
testDatafunc(net.call, testDataInput, testDataActual)

print "bfgs"
conec = mlgraph(networkFormation)
net = ffnet(conec)
net.train_bfgs(trainingSetInput[:learnData], trainingSetResult[:learnData])
testDatafunc(net.call, testDataInput, testDataActual)

print "cg"
conec = mlgraph(networkFormation)
net = ffnet(conec)
net.train_cg(trainingSetInput[:learnData], trainingSetResult[:learnData])
testDatafunc(net.call, testDataInput, testDataActual)

print "momentum"
conec = mlgraph(networkFormation)
net = ffnet(conec)
net.train_momentum(trainingSetInput[:learnData], trainingSetResult[:learnData])
testDatafunc(net.call, testDataInput, testDataActual)

print "rprop"
conec = mlgraph(networkFormation)
net = ffnet(conec)
net.train_rprop(trainingSetInput[:learnData], trainingSetResult[:learnData])
testDatafunc(net.call, testDataInput, testDataActual)

print "tnc"
conec = mlgraph(networkFormation)
net = ffnet(conec)
net.train_tnc(trainingSetInput[:learnData], trainingSetResult[:learnData])
testDatafunc(net.call, testDataInput, testDataActual)

print "Lasso Bitches!"
clf.fit(trainingSetInput[:learnData], trainingSetResult[:learnData])
testDatafunc(clf.predict, testDataInput, testDataActual)
#for each in zip(testDataInput, testDataActual):
#    predicted = clf.predict(each[0])
#    print "Actual: " + str(each[1]) + " Predict: " + str(predicted) + " Difference: " + str(math.fabs(each[1] - predicted))

#NX.draw(net.graph)
#pylab.show()
