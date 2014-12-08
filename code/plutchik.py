__author__ = 'giedomak'

import re

emotions = ("anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust")

regexes = []
for emotion in emotions:
    regexes.append((emotion,('|'.join(open('plutchik/'+emotion+'.txt', 'r').read().splitlines()))))

def executeTweet(tweet):
    res = []
    for regex in regexes:
     res.append(executeRegex(regex[1],tweet))
    return res

def executeRegex(emotionRegex, tweet):
    # get the regex from the emotion
    regex_tmp = emotionRegex
    regex_string = '(\W|^)('+regex_tmp+')(\W|$)'
    # print regex_string
    regex = re.compile(regex_string, re.IGNORECASE)

    # execute the regex on the tweet
    return str(len(regex.findall(tweet)))
