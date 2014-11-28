__author__ = 's138362'
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import codecs

ckey = 'Ac2Trdc9xU6pTz4v0SdGRURKH'
csecret = 'm29wgjcnLCcOTgQ5vQxjLK4i8bbSfls0qvaxj3iHQNvlelpNVl'
atoken = '2891995534-E78xGPCQnR34msGEIAujG1XlpsxRqxTzZcAeKhv'
asecret = 'icZjZQwjJEjgTEQJ2rlCy57cgY57a9Hb3EYBdjfB8CWDF'

TweetFile = codecs.open("Tweets.txt", "w", "utf-8")

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

class listener(StreamListener):

    def on_data(self, data):
         # Twitter returns data in JSON format - we need to decode it first
        if(data.startswith( '{"created_at":' )):
            decoded = json.loads(data)
            tweet = str((decoded['user']['screen_name'], decoded['text']))
            TweetFile.write(tweet)
            TweetFile.write("\n")
            print tweet
        else:
            return True
        return True

    def on_error(self, status):
        print status

twitterStream = Stream(auth, listener())
#twitterStream.sample(languages=["en"]);
twitterStream.filter(track=["Efteling"])
