#!/usr/bin/python


def readSentimentAnger(file_name):
    ifile = open(file_name, 'r')
    ifile.readline() #Ignore title row

    for line in ifile:
        print line


readSentimentAnger("plutchik/anger.txt")