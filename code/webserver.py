__author__ = 'max'

import web
import json
import pymongo
from datetime import *
import plutchik

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client.test_database
col = db.results
#today = datetime.today()
#delta = datetime.timedelta(days=-30)


urls = (
    '/', 'index',
    "/data", "getdata",
    "/plutchik", "getsentiment"

)



def convert_keys_to_string(dictionary):
    """Recursively converts dictionary keys to strings."""
    if not isinstance(dictionary, dict):
        return dictionary
    return dict((str(k).replace("\'", "\""), convert_keys_to_string(v))
        for k, v in dictionary.items())

class index:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        return "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


class getdata:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Content-Type', 'application/json')

        data = {}
        for i in range(250):
            date = (datetime.today() + timedelta(days=-i))
            date_key = str(date.day) + "/" + str(date.month) + "/" + str(date.year)
            try:
                data[date_key] = (convert_keys_to_string(col.find({'x':date_key}).next()))
                #data[-1]['x'] = str(data[-1]['x'])
                del data[date_key]["_id"]
                #data[-1] = json.dumps(data[-1])
            except:
                pass
        return json.dumps(data)

class getsentiment:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')

        senti = plutchik.executeTweet(web.input()["text"])
        return json.dumps({
            "joy":senti[0],
            "trust":senti[1],
            "fear":senti[2],
            "surprise":senti[3],
            "sadness":senti[4],
            "disgust":senti[5],
            "anger":senti[6],
            "anticipation":senti[7]
        })
        #return plutchik.executeTweet(web.input()["text"])




if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()



