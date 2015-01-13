__author__ = 'max'

import web
import json
from datetime import *
import plutchik



urls = (
    '/', 'index',
    "/plutchik", "getsentiment"
)


class index:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        return "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


class getsentiment:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')


        return plutchik.executeTweet(web.input()["text"])




if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()




