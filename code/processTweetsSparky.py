from pyspark import SparkContext
import datetime
import plutchik

def dateTimeAndPlutchik(tweet):
    date = datetime.datetime.strptime(tweet["created_at"], '%a %b %d %H:%M:%S +0000 %Y')
    key = str(date.month) + "/" + str(date.day)
    tweetMoods = plutchik.executeTweet(tweet["text"])
    return {"key": key, "moods": tweetMoods}

logFile = "C:\spark-1.2.0-bin-hadoop2.4/README.md"  # Should be some file on your system
sc = SparkContext("local", "GetRich")

#tweetData = sc.textFile(logFile).cache()
tweetData = sc.parallelize([
        {"created_at": "Mon Jan 05 01:05:03 +0000 2010", "text":"http://"},
        {"created_at": "Mon Jan 06 01:05:03 +0000 2010", "text":"blub RT"},
        {"created_at": "Mon Jan 08 01:05:03 +0000 2010", "text":"Guido RT zit naast mij"},
        {"created_at": "Mon Jan 08 01:05:03 +0000 2010", "text":"blubsa"},
        {"created_at": "Mon Jan 08 01:05:03 +0000 2010", "text":"RT Ik heb lol"},
        {"created_at": "Mon Jan 08 01:05:03 +0000 2010", "text":"RT Ik heb lol en boos"},
    ])

tweetData = tweetData.filter(lambda t: not("http://" in t["text"]) and "RT" in t["text"])
tweetData = tweetData.map(dateTimeAndPlutchik)
tweetData = tweetData.groupBy(lambda t: t["key"])

print tweetData.collect()

