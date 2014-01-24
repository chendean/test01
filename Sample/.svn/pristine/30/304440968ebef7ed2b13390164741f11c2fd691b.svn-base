#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
__version__ = "0.0"
__author__ = 'Dean'

from BigoCfgWeb import urls

#webset的基类
class WebBase:
    def __init__(self):
        return self.init()

    def GET(self):
        if(not 'login' in urls.session) or (not urls.session.login == 1):
            urls.session.kill()
            #重新登录
            return "<script type='text/javascript'>window.location.href = '\login'</script>"
        else:
            return self.get()

    def POST(self):
        return self.post()

    #__init__的接口
    def init(self):
        pass

    #GET的接口
    def get(self):
        pass

    #POST的接口
    def post(self):
        pass



