__author__ = 's138362'
import numpy as np
import json
import codecs


TweetFileHappy = codecs.open("TweetsHappy.txt", "w", "utf-8")
TweetFileNeutral = codecs.open("TweetsNeutral.txt", "w", "utf-8")
TweetFileSad = codecs.open("TweetsSad.txt", "w", "utf-8")



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
    tweet = data.split()
    # Here we have tweets which we have already tokenized (turned into an array of words)

    # Calculate the probabilities that the tweets are happy or sad
    tweet_happy_prob, tweet_sad_prob = classifySentiment(tweet, happy_log_probs, sad_log_probs)
    return tweet_sad_prob

happy_log_probs, sad_log_probs = readSentimentList('twitter_sentiment_list.csv')
    #print "The probability that tweet1 (", tweet, ") is happy is ", tweet_happy_prob, "and the probability that it is sad is ", tweet_sad_prob