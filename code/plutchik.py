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
# walking clockwise around the wheel, starting at the top
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

negations = ("n't", "0", "aint", "arent", "cant", "couldnt", "darent", "didnt", "doesnt", "dont", "hadnt", "hasnt", "havent",
             "isnt", "mightnt", "mustnt", "neednt", "never", "no", "not", "oughtnt", "shant", "shouldnt", "w/o", "wasnt",
             "werent", "without", "wont", "wouldnt", "zero")

def executeTweet(tweet):
    # prepare tweet
    tweet = tweet.replace("~",  "").replace("#", "").replace("_", "").replace("?",  "").replace("\"", "").replace("\'", "").replace("*",  "")

    # init result list
    res = [0 for x in range(len(emotions))]

    # get the number of hits per emotion for this tweet
    for index, emotion in enumerate(emotions):
        res[index] = executeRegex(emotion.regex, tweet)

    print res
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
executeTweet("tolera wear his heart on his sleeves")