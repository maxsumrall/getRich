from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from operator import add
import datetime
import plutchik
import pymongo
import time
import os

def dateTimeAndPlutchik(tweet):
    try:
        date = datetime.datetime.strptime(tweet[0], '%a %b %d %H:%M:%S +0000 %Y')
        key = str(date.month) + "/" + str(date.day)
        tweetMoods = plutchik.executeTweet(tweet[1])
        return key, tweetMoods
    except:
        # print "not a date"
        return "none", [0, 0, 0, 0, 0, 0, 0, 0]


def retrieve(t):
    client = pymongo.MongoClient('giedomak.nl')
    db = client.test_database
    tweets = db.tweets
    return tweets.find_one(None, None, t)

def split_tweet(t):
    result = t.split(';',1)
    result.extend([""])
    return result

def add_count_number(t):
    t[1].append(1)
    return t


logFile = "C:\spark-1.2.0-bin-hadoop2.4/README.md"  # Should be some file on your system
sc = SparkContext("local", "GetRich")
ssc = StreamingContext(sc, 1)
ssc.checkpoint("checkpoint")

stream = ssc.socketTextStream("localhost", 9999)
tweetData = stream.flatMap(lambda line: line.split("\r\n"))
# tweetData.pprint()

#tweetData = sc.textFile(logFile).cache()
# tweetData = sc.parallelize([
#         {"created_at": "Mon Jan 05 01:05:03 +0000 2010", "text":"http://"},
#         {"created_at": "Mon Jan 06 01:05:03 +0000 2010", "text":"blub RT"},
#         {"created_at": "Mon Jan 08 01:05:03 +0000 2010", "text":"Guido RT zit naast mij"},
#         {"created_at": "Mon Jan 08 01:05:03 +0000 2010", "text":"blubsa"},
#         {"created_at": "Mon Jan 08 01:05:03 +0000 2010", "text":"RT Ik heb lol"},
#         {"created_at": "Mon Jan 08 01:05:03 +0000 2010", "text":"RT Ik heb lol en boos"},
#         {"created_at": "Mon Jan 08 01:05:03 +0000 2010", "text":"RT Haat klote kut"},
#     ])

# client = pymongo.MongoClient('giedomak.nl')
# db = client.test_database
# tweets = db.tweets

# tweetdata = range(100)
# tweetdata = sc.parallelize(tweetdata)

#tweetdata = tweetdata.map(lambda t: tweets.find_one(None, None, t))
# tweetdata = tweetdata.map(retrieve)

# print tweetdata.collect()

tweetData = tweetData.map(split_tweet)
# tweetData.pprint()
# tweetData = tweetData.map(lambda s: (s[0], ''.join(str(x) for x in s[1:])))
# tweetData.pprint()
tweetData = tweetData.filter(lambda t: not("http" in t[1]) and "RT" in t[1])
# tweetData = tweetData.filter(lambda t: not("http" in t[1]) and "RT" in t[1])
# tweetData = tweetData.filter(lambda t: "RT" in t[1:])
# tweetData.pprint()

moodData = tweetData.map(dateTimeAndPlutchik)
# moodData.pprint()
moodData = moodData.filter(lambda t: not all(m == 0 for m in t[1]))
# moodData.pprint()
# print moodData.pprint()

# moodData.pprint()

moodData = moodData.map(add_count_number)
moodData.checkpoint(15)

# moodTotal = moodData.reduceByKey(lambda a, b: map(add, a, b))
# moodTotal = moodData.reduceByKeyAndWindow(lambda a, b: map(add, a, b), lambda a, b: a, 3, 2)
# moodTotal = moodData.reduceByKeyAndWindow(lambda a, b: map(add, a, b), None, 60*60)
# moodTotal = moodData.reduceByKeyAndWindow(lambda a, b: map(add, a, b), None, 7*60*60)
# moodCount = moodData.countByKey()     # No count in streaming API

def addToState(newMood, runningTotal):
    if(runningTotal is None):
        print newMood
        return newMood
    else:
        print map(add, newMood, runningTotal)
        return map(add, newMood, runningTotal)

moodTotal = moodData.updateStateByKey(addToState)

# moodDay = map(lambda a: (a[0], map(lambda b: b/moodCount[a[0]], a[1])), moodTotal.pprint())

#moodTotal.saveAsTextFiles("test")


def processResults(rdd):
    print rdd.collect()
    if(len(rdd.collect()) > 0):
        i = 0
        while os.path.isdir("testResults" + str(i)):
            i += 1
        rdd.saveAsTextFile("testResults" + str(i))
        print "results!!!!!!!!!!" + str(i)

moodTotal.foreachRDD(processResults)

moodTotal.pprint()
# moodCount.pprint()
# moodDay.pprint()

ssc.start()             # Start the computation
#raw_input('Press enter to close')
#time.sleep(10)
ssc.awaitTermination()  # Wait for the computation to terminate
#ssc.stop(stopSparkContext=True, stopGraceFully=True)
