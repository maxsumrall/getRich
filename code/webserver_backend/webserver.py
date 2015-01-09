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



class index:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        return "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


class data:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        data = []
        for i in range(30):
            date = (datetime.today - datetime.timedelta(days=-i))
            date_key = str(date.day) + "/" + str(date.month) + "/" + str(date.year)
            print date_key
            try:
                data.append(col.find({'x':date_key}).next())
            except:
                pass

        return data





if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()



