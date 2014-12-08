__author__ = 'giedomak'

import re

emotions = ("anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust")

regexes = []
for emotion in emotions:
    # create regexes with their emotions
    inner_regex = ('|'.join(open('plutchik/'+emotion+'.txt', 'r').read().splitlines()))
    regex_tmp = '(\W|^)(' + inner_regex + ')(\W|$)'
    regexes.append((emotion, regex_tmp))

def executeTweet(tweet):
    res = []
    for regex in regexes:
        # execute the regex on the tweet for each emotion
        res.append(executeRegex(regex[1], tweet))
    return res

def executeRegex(regex_string, tweet):
    # compile the regex with the flag IGNORECASE
    regex = re.compile(regex_string, re.IGNORECASE)

    # execute the regex on the tweet
    result = regex.findall(tweet)

    # return length of the results array, this should be the number of occurrences of emotion terms
    return len(result)
