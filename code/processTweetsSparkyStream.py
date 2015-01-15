import pymongo
import socket
import sys
import datetime
import codecs
import chardet

def SendTweets():
    TCP_IP = '127.0.0.1'
    TCP_PORT = 9998

    # command line parameters
    # use processTweets.py -m to use localhost mongodb, else giedomak.nl mongodb will be used
    # use processTweets.py -n 1000 to process 1000 tweets, else all will be done
    # use processTweets.py -ip 127.0.0.1 to send all tweets too 127.0.0.1
    # use processTweets.py -port 5005 to send all tweets to port 5005
    if "-m" in sys.argv:
        print "local mongodb"
        client = pymongo.MongoClient()
    else:
        print "giedomak.nl mongodb"
        client = pymongo.MongoClient('giedomak.nl')

    if "-n" in sys.argv:
        total = int(sys.argv[sys.argv.index("-n")+1])
    else:
        total = -1

    if "-ip" in sys.argv:
        TCP_IP = sys.argv[sys.argv.index("-ip")+1]

    if "-port" in sys.argv:
        TCP_PORT = int(sys.argv[sys.argv.index("-port")+1])

    print "get tweets"
    db = client.test_database
    tweets = db.tweets

    if total > 0:
        tweetlist = tweets.find(limit=total)
    else:
        tweetlist = tweets.find().sort('_id', -1)
        total = tweets.count()

    print "Start TCP server"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(None)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)


    #while 1:
    print "Waiting for client..."
    conn, addr = s.accept()
    print 'Connection address:', addr

    print "Sending tweets..."
    n = 0
    startTime = datetime.datetime.now()
    print "Start time: " + str(startTime)


    for tweet in tweetlist:

        try:
            result = str(tweet["created_at"] + ";" + tweet["text"].replace("\r", " ").replace("\n", " ") + "\r\n")
            conn.send(result)

        except:

            try:
                result = str('{dt:%a} {dt:%b} {dt:%d} {dt:%H}:{dt:%M}:{dt:%S} +0000 {dt:%Y}'.format(dt=tweet['_id'].generation_time) + ";" + tweet["text"].replace("\r", " ").replace("\n", " ") + "\r\n")
                conn.send(result)

            except:
                1==1

        n = n + 1
        if n%100000 == 0:
            currentTime = datetime.datetime.now()
            differenceTime = currentTime-startTime
            remainingTime = differenceTime/n*(total-n)
            endTime = currentTime+remainingTime
            print "Send " + str(n) + "/" + str(total) + " tweets... (running time: " + str(differenceTime) + ", remaining time: " + str(remainingTime) + ", end time: " + str(endTime) + ")"

    conn.close()
    print "Tweets send"
    s.close()

if __name__ == "__main__":
    while 1:
        SendTweets()
