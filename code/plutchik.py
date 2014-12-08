__author__ = 'giedomak'

import re

def getPlutchik(tweet):


    return 0

def executeTweet(tweet):
    print tweet
    executeRegex('anger', tweet)
    executeRegex('anticipation', tweet)
    executeRegex('disgust', tweet)
    executeRegex('fear', tweet)
    executeRegex('joy', tweet)
    executeRegex('sadness', tweet)
    executeRegex('surprise', tweet)
    executeRegex('trust', tweet)
    print ''

def executeRegex(emotion, tweet):
    # get the regex from the emotion
    regex_tmp = '|'.join(open('plutchik/'+emotion+'.txt', 'r').read().splitlines())
    regex_string = '(\W|^)('+regex_tmp+')(\W|$)'
    # print regex_string
    regex = re.compile(regex_string, re.IGNORECASE)

    # execute the regex on the tweet
    print emotion + ": " + str(len(regex.findall(tweet)))
    return


executeTweet('I am not as good as I thought. At least, I am in love and get laid everyday')
executeTweet('oh no #fml')
executeTweet('Fuck the rest of my sunny life')
executeTweet('yeah')