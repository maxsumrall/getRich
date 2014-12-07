#!/usr/bin/python

import os, json, subprocess, pymongo, GetRich
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
			sumToday += sentiment(tweet["text"])
			countToday += 1.0
			days[key] = (sumToday, countToday)
	for key in days.keys():
		print key + ": " + str(days[key][0]/days[key][1])
			






def sentiment(tweet):
	return 0.4


def countEmotWords():
	count = 0
	for tweet in tweets.find():
		if len(set(tweet["text"].lower().split()) & emotional_words_filter_set) > 0:
			count += 1
	print count


calculateAverageSentiment()
