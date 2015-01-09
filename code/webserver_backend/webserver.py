__author__ = 'max'

import web
import json
import pymongo
from datetime import *

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client.test_database
col = db.results
#today = datetime.today()
#delta = datetime.timedelta(days=-30)


urls = (
    '/', 'index',
    "/data", "data"
)

data_file_name = "data.json"
data_file = open(data_file_name, 'r')
json_data = data_file.read().replace("\n", "")
#data = json.load(data_file)
#data_file.close()


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


class data:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        data = []
        for i in range(30):
            date = (datetime.today() + timedelta(days=-i))
            date_key = str(date.day) + "/" + str(date.month) + "/" + str(date.year)
            print date_key
            try:
                data.append(convert_keys_to_string(col.find({'x':date_key}).next()))
                data[-1]['x'] = str(data[-1]['x'])
            except:
                pass

        return data





if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()



