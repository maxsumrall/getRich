__author__ = 's138362'
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

ckey = 'Ac2Trdc9xU6pTz4v0SdGRURKH'
csecret = 'm29wgjcnLCcOTgQ5vQxjLK4i8bbSfls0qvaxj3iHQNvlelpNVl'
atoken = '2891995534-E78xGPCQnR34msGEIAujG1XlpsxRqxTzZcAeKhv'
asecret = 'icZjZQwjJEjgTEQJ2rlCy57cgY57a9Hb3EYBdjfB8CWDF'

class listener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["Samsung"])