__author__ = 'max'

import web
import json
urls = (
    '/', 'index',
    "/data", "data"
)

data_file_name = "data.json"
data_file = open(data_file_name, 'r')
data = data_file.read().replace("\n", "")
#data = json.load(data_file)
#data_file.close()



class index:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        return "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


class data:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        return json.dumps(data)



if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()



