__author__ = 'Grabot'

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import plutchik

#For getting twitter stream we created a twitter dev account that will allow us to use the API
#For this you need the customer key customer secret authentication token and authentication tokan
#these are provided in your development account and placed here in the code
ckey = 'Ac2Trdc9xU6pTz4v0SdGRURKH'
csecret = 'm29wgjcnLCcOTgQ5vQxjLK4i8bbSfls0qvaxj3iHQNvlelpNVl'
atoken = '2891995534-E78xGPCQnR34msGEIAujG1XlpsxRqxTzZcAeKhv'
asecret = 'icZjZQwjJEjgTEQJ2rlCy57cgY57a9Hb3EYBdjfB8CWDF'

#we create the authentication for the twitter stream getting
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

class listener(StreamListener):
    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first using user name and the tweet text
        if (data.startswith('{"created_at":')):
            decoded = json.loads(data)
            tweet = str((decoded['user']['screen_name'], decoded['text']))
            #we send the tweet to the mood analyser who will determine the mood of the tweet based on plutchik
            print plutchik.executeTweet(tweet)

        return True

    def on_error(self, status):
        print status

#create and run the stream, we only select english tweets.
twitterStream = Stream(auth, listener())
twitterStream.sample(languages=["en"])