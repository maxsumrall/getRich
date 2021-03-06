from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from operator import add
import datetime
import plutchik
import pymongo
import time
import os
import processTweetsSparkyStream
import ystockquote
import sys

def dateTimeAndPlutchik(tweet):
    try:
        date = datetime.datetime.strptime(tweet[0], '%a %b %d %H:%M:%S +0000 %Y')
        # key = str(date.day) + "/" + str(date.month) + "/" + str(date.year)
        key = '{dt:%x}'.format(dt=date)
        tweetMoods = plutchik.executeTweet(tweet[1])
        return key, tweetMoods
    except:
        # print "not a date"
        return "none", [0, 0, 0, 0, 0, 0, 0, 0]

def split_tweet(t):
    result = t.split(';',1)
    result.extend([""])
    return result

def add_count_number(t):
    t[1].append(1)
    return t

def addToState(newMood, runningTotal):
    if(runningTotal is None):
        return reduce(lambda a, b: (map(add, a, b)), newMood, [0, 0, 0, 0, 0, 0, 0, 0, 0])
    else:
        return map(add, reduce(lambda a, b: (map(add, a, b)), newMood, [0, 0, 0, 0, 0, 0, 0, 0, 0]), runningTotal)

def makeJson(line):
    date_y = '{dt.year}-{dt:%m}-{dt:%d}'.format(dt=datetime.datetime.strptime(line[0], '%x'))
    date_json = '{dt.day}/{dt.month}/{dt.year}'.format(dt=datetime.datetime.strptime(line[0], '%x'))

    try:
        ystock_dict = ystockquote.get_historical_prices("^IXIC",date_y,date_y)
        ystock = ystock_dict[date_y]["Close"] if ystock_dict[date_y] else 0
    except:
        ystock = 0

    return {'x': date_json, '_id':date_json, 'joy':line[1][0]/line[1][8], 'trust':line[1][1]/line[1][8], 'fear':line[1][2]/line[1][8],
    'surprise':line[1][3]/line[1][8], 'sadness':line[1][4]/line[1][8], 'disgust':line[1][5]/line[1][8],
    'anger':line[1][6]/line[1][8], 'anticipation':line[1][7]/line[1][8],
    'prediction':0, 'Stock':ystock, 'total':line[1][8]}

def processResults(rdd):
    print rdd.collect()
    if(len(rdd.collect()) > 0):
        # Put it in MongoDB!
        if "-m" in sys.argv:
            client = pymongo.MongoClient()
        else:
            client = pymongo.MongoClient('giedomak.nl')
        db = client.test_database
        col = db.results
        for line in rdd.collect():
            result = makeJson(line)
            print result
            col.save(result)

logFile = "C:\spark-1.2.0-bin-hadoop2.4/README.md"  # Should be some file on your system
sc = SparkContext("local[4]", "GetRich")
ssc = StreamingContext(sc, 1)
ssc.checkpoint("checkpoint")

stream = ssc.socketTextStream("localhost", 9998)
tweetData = stream.flatMap(lambda line: line.split("\r\n"))

tweetData = tweetData.map(split_tweet)
#totalTweetsPerDay = tweetData.map(lambda a: (0, 1)).updateStateByKey(lambda a, running: (sum(a)+(running or 0)))


tweetData = tweetData.filter(lambda t: not("http" in t[1]) and "RT" in t[1])

moodData = tweetData.map(dateTimeAndPlutchik)
moodData = moodData.filter(lambda t: not all(m == 0 for m in t[1]))
moodData = moodData.map(add_count_number)
moodData.checkpoint(15)

moodTotal = moodData.reduceByKey(lambda a, b: map(add, a, b)).updateStateByKey(addToState)

moodTotal.foreachRDD(processResults)

moodTotal.pprint()

#def printValue(a):
#    print a.collect()
#totalTweetsPerDay.foreachRDD(printValue)

ssc.start()             # Start the computation
#raw_input('Press enter to close')
#time.sleep(30)
#ssc.awaitTermination()  # Wait for the computation to terminate
processTweetsSparkyStream.SendTweets()
ssc.stop(stopSparkContext=True, stopGraceFully=True)
