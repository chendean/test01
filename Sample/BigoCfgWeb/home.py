__author__ = 'Leon'
#coding:utf-8

import web
from web.contrib.template import render_mako
from BigoCommon import base
import BigoCommon.db
import hashlib
import urls

render = render_mako(
    directories=['templates'],
    input_encoding='utf-8',
    output_encoding='utf-8',
)

class home(base.WebBase):
    def get(self):
    #render画面对象
        return render.home()

    def post(self):
        pass