__author__ = 'giedomak'

import re

def getPlutchik(tweet):


    return 0

def executeRegex(emotion, tweet):
    # get the regex from the emotion
    regex = re.compile('|'.join(open('plutchik/'+emotion+'.txt', 'r').read().splitlines()))

    # execute the regex on the tweet
    match = regex.search(tweet)
    regex.match(tweet)
    if match:
        print emotion + ": " + str(len(match.groups()))
    return

tweet = 'I am not as good as I thought. At least, I am in love and get laid everyday'
executeRegex('anger', tweet)
executeRegex('anticipation', tweet)
executeRegex('disgust', tweet)
executeRegex('fear', tweet)
executeRegex('joy', tweet)
executeRegex('sadness', tweet)
executeRegex('surprise', tweet)
executeRegex('trust', tweet)
