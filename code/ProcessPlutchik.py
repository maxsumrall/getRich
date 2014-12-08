#!/usr/bin/python

def readSentimentList(file_name):
    ifile = open(file_name, 'r')
    happy_log_probs = {}
    sad_log_probs = {}
    ifile.readline() #Ignore title row

    for line in ifile:
        print line

    return line

readSentimentList("TweetsHappy.txt")