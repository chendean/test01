__author__ = 'leon'
#coding:utf-8
import web
try:
    import simplejson as json
except ImportError:
    import json
import mimerender

ds = mimerender.WebPyMimeRender()

render_xml = lambda message: '<message>%s</message>'%message
render_json = lambda **args: json.dumps(args)
render_html = lambda message: '<html><body>%s</body></html>'%message
render_txt = lambda message: message

urls = (
    '/(.*)', 'greet'
    )
app = web.application(urls, globals())

class greet:
    @ds(
        default = 'xml',
        html = render_html,
        xml  = render_xml,
        json = render_json,
        txt  = render_txt
    )
    def GET(self, name):
        if not name:
            name = 'world'
        return {'message': 'Hello, ' + name + '!'}

    def POST(self, name):
        data = web.data()
        localOrderInfos = json.loads(data)
        if not name:
            name = 'world'
        return {'message': 'Hello, ' + name + '!' }
if __name__ == "__main__":
    app.run()