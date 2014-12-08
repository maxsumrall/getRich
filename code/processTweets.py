#!/usr/bin/python

import os, json, subprocess, pymongo, Sentiment
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
    currDay = 0
    countToday = 1.0
    days = {}
    for tweet in tweets.find():
        if len(set(tweet["text"].lower().split()) & emotional_words_filter_set) > 0:
            date = datetime.strptime(tweet["created_at"], '%a %b %d %H:%M:%S +0000 %Y')
            key = str(date.month) + "/" + str(date.day)
            #tweetMoods = Sentiment.Sentiment(tweet["text"])
            tweetMoods = (0.4,0.5,0.6,0.7,0.3,0.2,0.1)
            if key in days.keys():
                for i in range(len(tweetMoods)):
                    days[key][0][i] += tweetMoods[i]
            else:
                sentiments = [tweetMoods[0],tweetMoods[1],tweetMoods[2],tweetMoods[3],tweetMoods[4],tweetMoods[5],tweetMoods[6]]
                days[key] = [sentiments, 1.0]


    print "day,mood1,mood2,mood3.mood4,mood5,mood6,mood7"
    for key in days.keys():
        sentiments, count = days[key]
        print key \
              + "," + str(sentiments[0] / count) \
              + "," + str(sentiments[1] / count) \
              + "," + str(sentiments[2] / count) \
              + "," + str(sentiments[3] / count) \
              + "," + str(sentiments[4] / count) \
              + "," + str(sentiments[5] / count) \
              + "," + str(sentiments[6] / count)

def countEmotWords():
    count = 0
    for tweet in tweets.find():
        if len(set(tweet["text"].lower().split()) & emotional_words_filter_set) > 0:
            count += 1
    print count


calculateMoodsSentiment()
