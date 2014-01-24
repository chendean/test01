__author__ = 'leon'
#coding:utf-8

import web
import json
render = web.template.render('templates')
db = web.database(dbn = 'mysql', db = 'test', user = 'leon', pw = 'zaq12wsx',host='192.168.0.32', port=3306)
urls = (
    '/', 'index'
    )

class index:
    def GET(self):
        todos = db.select('todo')

        return render.sample1(todos)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

