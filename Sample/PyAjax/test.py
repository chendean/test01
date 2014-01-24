__author__ = 'leon'
#coding:utf-8

import web
import json
render = web.template.render('templates')

urls = (
    '/index', 'index',
    '/ResultsHandler', 'ResultsHandler',
    )

class index:
    def GET(self):
        return render.testAjax()

class ResultsHandler():

    def POST(self):

        output ={"salary":"123456"}
        output = json.dumps(output) #json encoding
        #print output
        return output

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()