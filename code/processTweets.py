#!/usr/bin/python

import os, json, subprocess, pymongo, plutchik, Sentiment, threading, sys,time,datetime , subprocess, re

# command line parameters
# use processTweets.py -m to use localhost mongodb, else giedomak.nl mongodb will be used
# use processTweets.py -n 1000 to process 1000 tweets, else all will be done
if "-m" in sys.argv:
    print "local mongodb"
    client = pymongo.MongoClient()
else:
    print "giedomak.nl mongodb"
    client = pymongo.MongoClient('giedomak.nl')

db = client.test_database
tweets = db.tweets
results_collection = db.results
if "-n" in sys.argv:
    total = int(sys.argv[sys.argv.index("-n")+1])
else:
    total = tweets.count()

tweetNumber = 0
done = False
tweetMatch = 0
finish = False

days = {}
print "Processing " + str(total) + " tweets"


def printit():
    if not finish:
        threading.Timer(5.0, printit).start()
        sys.stdout.write("\r%6.2f%% Tweets filtered out: %6.2f%%" % ((tweetNumber/float(total)*100), ((1-(tweetMatch/float(tweetNumber+1)))*100)))


def calculateMoodsSentiment():
    try:
        global tweetMatch
        global tweetNumber
        global days
        # print "Number of tweets: " + str(tweets.count())
        for tweet in tweets.find()[:total]:
            # for printing progress
            tweetNumber += 1

            # only process tweets that don't have http:// in there
            # if len(http_regex.findall(tweet["text"])) is 0:
            # print tweet["text"][:2]
            if tweet["text"].find("http://") is -1 and tweet["text"][:2] == "RT":
                # print tweet["text"]
                tweetMatch += 1

                date = datetime.datetime.strptime(tweet["created_at"], '%a %b %d %H:%M:%S +0000 %Y')
                key = str(date.month) + "/" + str(date.day)
                tweetMoods = plutchik.executeTweet(tweet["text"])
                if key in days.keys():
                    days[key][1] += 1
                    for i in range(len(tweetMoods)):
                        days[key][0][i] += tweetMoods[i]
                else:
                    days[key] = [tweetMoods, 1.0]

            # else:
            #     print "http found: " + unicode(tweet["text"]).encode('utf-8')

        outfile_name = "output_results" + str(time.time()).replace(".","_") + ".csv"
        outfile = open(outfile_name,"w")
        line = "day,joy,trust,fear,surprise,sadness,disgust,anger,anticipation"
        print "\n\n" + line
        outfile.writelines(line + "\n")
        for key in days.keys():
            sentiments, count = days[key]
            line = key \
                  + "," + str(sentiments[0] / count) \
                  + "," + str(sentiments[1] / count) \
                  + "," + str(sentiments[2] / count) \
                  + "," + str(sentiments[3] / count) \
                  + "," + str(sentiments[4] / count) \
                  + "," + str(sentiments[5] / count) \
                  + "," + str(sentiments[6] / count) \
                  + "," + str(sentiments[7] / count)
            print line
            outfile.writelines(line + "\n")

        # normalize: (Xi - min(X)) / (max(X) - min(X))
        avg = []
        for key in days.keys():
            sentiments, count = days[key]
            avg.append((key, [(sentiments[0] / count), (sentiments[1] / count), (sentiments[2] / count), (sentiments[3] / count), (sentiments[4] / count), (sentiments[5] / count), (sentiments[6] / count), (sentiments[7] / count)]))
        max = 0.0
        min = 10000.0
        for day in avg:
            for emotion in day[1]:
                if emotion > max:
                    max = emotion
                if emotion < min:
                    min = emotion

        # min and max calculated
        for i in range(len(avg)):
            for j in range(len(avg[i][1])):
                avg[i][1][j] = (avg[i][1][j] - min) / (max - min)
        line = "day,joy,trust,fear,surprise,sadness,disgust,anger,anticipation"
        outfile.writelines(line + "\n")
        print
        for day in avg:
            line = day[0] \
                  + "," + str(day[1][0]) \
                  + "," + str(day[1][1]) \
                  + "," + str(day[1][2]) \
                  + "," + str(day[1][3]) \
                  + "," + str(day[1][4]) \
                  + "," + str(day[1][5]) \
                  + "," + str(day[1][6]) \
                  + "," + str(day[1][7])
            print line
            outfile.writelines(line + "\n")
        outfile.close()
        subprocess.check_output("cp "+outfile_name + " output.csv", shell=True)


        # for frontend
        labels = []
        for key in days.keys():
            labels.append(key)

        sentiment = [[] for x in range(8)]
        for key in days.keys():
            sentiments, count = days[key]
            for i in range(len(sentiment)):
                sentiment[i].append(sentiments[i]/count)

        print labels
        print sentiment

        results_collection.insert(days)
        outfile.close()

    except KeyboardInterrupt:
        global finish
        finish = True

printit()
calculateMoodsSentiment()
finish = True