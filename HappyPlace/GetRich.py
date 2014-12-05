__author__ = 's138362'
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import numpy as np
import json
import codecs

ckey = 'Ac2Trdc9xU6pTz4v0SdGRURKH'
csecret = 'm29wgjcnLCcOTgQ5vQxjLK4i8bbSfls0qvaxj3iHQNvlelpNVl'
atoken = '2891995534-E78xGPCQnR34msGEIAujG1XlpsxRqxTzZcAeKhv'
asecret = 'icZjZQwjJEjgTEQJ2rlCy57cgY57a9Hb3EYBdjfB8CWDF'

TweetFileHappy = codecs.open("TweetsHappy.txt", "w", "utf-8")
TweetFileNeutral = codecs.open("TweetsNeutral.txt", "w", "utf-8")
TweetFileSad = codecs.open("TweetsSad.txt", "w", "utf-8")

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

def readSentimentList(file_name):
    ifile = open(file_name, 'r')
    happy_log_probs = {}
    sad_log_probs = {}
    ifile.readline() #Ignore title row

    for line in ifile:
        tokens = line[:-1].split(',')
        happy_log_probs[tokens[0]] = float(tokens[1])
        sad_log_probs[tokens[0]] = float(tokens[2])

    return happy_log_probs, sad_log_probs

def classifySentiment(words, happy_log_probs, sad_log_probs):
    # Get the log-probability of each word under each sentiment
    happy_probs = [happy_log_probs[word] for word in words if word in happy_log_probs]
    sad_probs = [sad_log_probs[word] for word in words if word in sad_log_probs]

    # Sum all the log-probabilities for each sentiment to get a log-probability for the whole tweet
    tweet_happy_log_prob = np.sum(happy_probs)
    tweet_sad_log_prob = np.sum(sad_probs)

    # Calculate the probability of the tweet belonging to each sentiment
    prob_happy = np.reciprocal(np.exp(tweet_sad_log_prob - tweet_happy_log_prob) + 1)
    prob_sad = 1 - prob_happy

    return prob_happy, prob_sad

def Sentiment(data):
    # We load in the list of words and their log probabilities
    happy_log_probs, sad_log_probs = readSentimentList('twitter_sentiment_list.csv')

    tweet = data.split()
    # Here we have tweets which we have already tokenized (turned into an array of words)

    # Calculate the probabilities that the tweets are happy or sad
    tweet_happy_prob, tweet_sad_prob = classifySentiment(tweet, happy_log_probs, sad_log_probs)

    if( tweet_happy_prob >= 0.5 and tweet_happy_prob < 0.7):
        output = "the tweet is neutral: ", tweet_happy_prob, " tweet: ", data
        TweetFileNeutral.write("the tweet is neutral: ")
        TweetFileNeutral.write(str(tweet_happy_prob))
        TweetFileNeutral.write(" tweet: ")
        TweetFileNeutral.write(data)
        TweetFileNeutral.write("\n")
        print output

    if( tweet_happy_prob >= 0.7 ):
        output = "the tweet is happy: ", tweet_happy_prob, " tweet: ", data
        TweetFileHappy.write("the tweet is happy: ")
        TweetFileHappy.write(str(tweet_happy_prob))
        TweetFileHappy.write(" tweet: ")
        TweetFileHappy.write(data)
        TweetFileHappy.write("\n")
        print output

    if( tweet_happy_prob < 0.5 ):
        output = "the tweet is sad: ", tweet_sad_prob, " tweet: ", data
        TweetFileSad.write("the tweet is sad: ")
        TweetFileSad.write(str(tweet_happy_prob))
        TweetFileSad.write(" tweet: ")
        TweetFileSad.write(data)
        TweetFileSad.write("\n")
        print output


    #print "The probability that tweet1 (", tweet, ") is happy is ", tweet_happy_prob, "and the probability that it is sad is ", tweet_sad_prob

class listener(StreamListener):

    def on_data(self, data):
         # Twitter returns data in JSON format - we need to decode it first
        if(data.startswith( '{"created_at":' )):
            decoded = json.loads(data)
            tweet = str((decoded['user']['screen_name'], decoded['text']))
            #TweetFile.write(tweet)
            #TweetFile.write("\n")
            Sentiment(tweet)
        else:
            return True
        return True

    def on_error(self, status):
        print status

twitterStream = Stream(auth, listener())
twitterStream.sample(languages=["en"]);
#twitterStream.filter(languages=["en"])
