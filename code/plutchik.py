__author__ = 'giedomak'

import re

# workflow:
# 1. get regular expressions from the emotion files
# 2. compile this regex and the opposite regex
# 3. match regex on the tweet
# 4. normalize the results


negations = ("n't", "0", "aint", "arent", "cant", "couldnt", "darent", "didnt", "doesnt", "dont", "hadnt", "hasnt", "havent",
             "isnt", "mightnt", "mustnt", "neednt", "never", "no", "not", "oughtnt", "shant", "shouldnt", "w/o", "wasnt",
             "werent", "without", "wont", "wouldnt", "zero")
negationPatern = '(' + ('|'.join(negations)) + ')\W'


class Emotion:
    def __init__(self, name):
        self.name = name
        self.getRegex()

    def getRegex(self):
        # load and create regexes
        inner_patern = ('|'.join(open('plutchik/'+self.name+'.txt', 'r').read().splitlines()))
        pattern = '(' + inner_patern + ')'
        self.regex = re.compile(pattern, re.IGNORECASE)
        self.negationRegex = re.compile(negationPatern + inner_patern, re.IGNORECASE)


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


def executeTweet(tweet):
    # prepare tweet
    tweet = tweet.replace("~",  "").replace("#", "").replace("_", "").replace("?",  "").replace("\"", "").replace("\'", "").replace("*",  "")

    # init result list
    res = [0.0 for x in range(len(emotions))]

    # get the number of hits per emotion for this tweet
    # also get the number op negation hits
    for index, emotion in enumerate(emotions):
        val1 = executeRegex(emotion.regex, tweet)
        val2 = executeRegex(emotion.negationRegex, tweet)

        # print "Negations: " + str(val2)

        # get the opposite emotion index
        oppositeIndex = index + 4
        if oppositeIndex > 7:
            oppositeIndex -= 8

        # if the difference is still positive, add it to the emotions value
        if val1 - val2 > 0:
            res[index] += val1 - val2

        # add the opposite value to the opposite emotion
        res[oppositeIndex] += val2

    # normalize the values
    # get the total of hits
    total = 0.0
    for result in res:
        total += result

    # divide each count with the total
    if total:
        res[:] = [result / total for result in res]

    # print res
    return res


def executeRegex(regex, tweet):
    # execute the regex on the tweet
    result = regex.findall(tweet)

    # return length of the results array, this should be the number of occurrences of emotion terms
    # print result
    return len(result)

# testing stuff
# executeTweet("tolera wear his heart on his sleeves but fear fear")