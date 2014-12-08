__author__ = 'giedomak'

import re

# workflow:
# 1. get regular expressions from the files
# 2. match regex on the tweet
# 3. normalize the results

class Emotion:
    name = ""
    regex = ""

    def __init__(self, name):
        self.name = name
        self.getRegex()

    def getRegex(self):
        # load and create regexes
        inner_regex = ('|'.join(open('plutchik/'+self.name+'.txt', 'r').read().splitlines()))
        self.regex = '(' + inner_regex + ')'

    def getOppositeEmotion(self):
        if self.name is 'joy':
            return "sadness"
        elif self.name is 'trust':
            return 'disgust'
        elif self.name is 'fear':
            return 'anger'
        elif self.name is 'surprise':
            return 'anticipation'
        elif self.name is 'sadness':
            return 'joy'
        elif self.name is 'disgust':
            return 'trust'
        elif self.name is 'anger':
            return 'fear'
        elif self.name is 'anticipation':
            return 'surprise'


# list with the emotions
emotions = [
    Emotion("joy"),
    Emotion("trust"),
    Emotion("fear"),
    Emotion("surprise"),
    Emotion("sadness"),
    Emotion("disgust"),
    Emotion("anger"),
    Emotion("anticipation")
    ]

def executeTweet(tweet):
    # init
    res = [0 for x in range(len(emotions))]

    for emotion in emotions:
        # execute the regex on the tweet for each emotion
        res.append(executeRegex(emotion.regex, tweet))
    # print res
    return res

def executeRegex(regex_string, tweet):
    # compile the regex with the flag IGNORECASE
    regex = re.compile(regex_string, re.IGNORECASE)

    # execute the regex on the tweet
    result = regex.findall(tweet)

    # return length of the results array, this should be the number of occurrences of emotion terms
    # print result
    return len(result)

# testing stuff
# executeTweet("tolera wear his heart on his sleeves")