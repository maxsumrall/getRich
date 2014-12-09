#!/usr/bin/python

import os, json, subprocess, pymongo, plutchik, Sentiment, threading
from datetime import *

client = pymongo.MongoClient()
db = client.test_database
tweets = db.tweets

emotional_words_filter = ["i feel", "i am feeling",
                          "i'm feeling", "im feeling",
                          "i don't feel",
                          "i dont feel", "i'm",
                          "im", "i am",
                          "makes me"]
emotional_words_filter_set = set(emotional_words_filter)
tweetNumber = 0

def printit():
    threading.Timer(5.0, printit).start()
    sys.stdout.write("\r%d%%" % (tweetNumber/float(tweets.count()))*100)

def calculateAverageSentiment():
    currDay = 0
    sumToday = 0.0
    countToday = 1.0
    days = {}
    for tweet in tweets.find():
        if len(set(tweet["text"].lower().split()) & emotional_words_filter_set) > 0:
            date = datetime.strptime(tweet["created_at"], '%a %b %d %H:%M:%S +0000 %Y')
            key = str(date.month) + "/" + str(date.day)
            if key in days.keys():
                sumToday, countToday = days[key]
            else:
                sumToday, countToday = (0.0, 0.0)
            sumToday += Sentiment.Sentiment(tweet["text"])
            countToday += 1.0
            days[key] = (sumToday, countToday)
    for key in days.keys():
        print key + ", " + str(days[key][0] / days[key][1])


def calculateMoodsSentiment():
    global tweetNumber
    days = {}
    for tweet in tweets.find():
        tweetNumber += 1
        if len(set(tweet["text"].lower().split()) & emotional_words_filter_set) > 0:
            date = datetime.strptime(tweet["created_at"], '%a %b %d %H:%M:%S +0000 %Y')
            key = str(date.month) + "/" + str(date.day)
            tweetMoods = plutchik.executeTweet(tweet["text"])
            if key in days.keys():
                days[key][1] += 1
                for i in range(len(tweetMoods)):
                    days[key][0][i] += tweetMoods[i]
            else:
                days[key] = [tweetMoods, 1.0]

    print "day,joy,trust,fear,surprise,sadness,disgust,anger,anticipation"
    for key in days.keys():
        sentiments, count = days[key]
        print key \
              + "," + str(sentiments[0] / count) \
              + "," + str(sentiments[1] / count) \
              + "," + str(sentiments[2] / count) \
              + "," + str(sentiments[3] / count) \
              + "," + str(sentiments[4] / count) \
              + "," + str(sentiments[5] / count) \
              + "," + str(sentiments[6] / count) \
              + "," + str(sentiments[7] / count)

    #normalize
    avg = []
    for key in days.keys():
        sentiments, count = days[key]
        avg.append((key, [(sentiments[0] / count), (sentiments[1] / count), (sentiments[2] / count), (sentiments[3] / count), (sentiments[4] / count), (sentiments[5] / count), (sentiments[6] / count), (sentiments[7] / count)]))
    max = 0
    min = 10000
    for day in avg:
        for emotion in day[1]:
            if emotion > max:
                max = emotion
            if emotion < min:
                min = emotion
    #min and max calculated
    for i in range(len(avg)):
        for j in range(len(avg[i][1])):
            avg[i][1][j] = (avg[i][1][j] - min) / (max - min)
    print "day,joy,trust,fear,surprise,sadness,disgust,anger,anticipation"
    for day in avg:
        print day[0] \
              + "," + str(day[1][0]) \
              + "," + str(day[1][1]) \
              + "," + str(day[1][2]) \
              + "," + str(day[1][3]) \
              + "," + str(day[1][4]) \
              + "," + str(day[1][5]) \
              + "," + str(day[1][6]) \
              + "," + str(day[1][7])



def countEmotWords():
    count = 0
    for tweet in tweets.find():
        if len(set(tweet["text"].lower().split()) & emotional_words_filter_set) > 0:
            count += 1
    print count


calculateMoodsSentiment()
