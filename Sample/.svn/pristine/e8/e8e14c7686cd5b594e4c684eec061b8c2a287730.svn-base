__author__ = 'leon'
#coding:utf-8

import web
from web.contrib.template import render_mako
import BigoCommon.db
import hashlib
import urls


db = BigoCommon.db.database(dbn='sqlite', db='db\BigoCfgDb.db')

def logged():
    if urls.session is None:
        return False
    else:
        if urls.session.login == 1:
            return True
        else:
            return False

#根据权限来控制登录
def create_render(is_superuser):
    render=None
    if logged():
        if is_superuser == 1:
            render = render_mako(
                directories=['templates'],
                input_encoding='utf-8',
                output_encoding='utf-8',
            )
        else:
            render = render_mako(
                directories=['templates'],
                input_encoding='utf-8',
                output_encoding='utf-8',
            )
    else:
        render = render_mako(
            directories=['templates'],
            input_encoding='utf-8',
            output_encoding='utf-8',
        )
    return render

class Login:
    def GET(self):
        if logged():
            render = create_render(urls.session.is_superuser)
            return  u"重复登录！"
        else:
            render = create_render(urls.session.is_superuser)
            return  render.login(msg=u'')

    def POST(self):
        name, passwd = web.input().username, web.input().password
        rtvalue=db.select('auth_user', where='username=$name', vars=locals())
        #数据库无返回则报错
        if rtvalue==None or rtvalue==[]:
            urls.session.login = 0
            urls.session.is_superuser = 0
            render = create_render(urls.session.is_superuser)
            #todo 需要改成读取配置
            return render.login(msg=u'密码错误！请重新输入！')
        else:
            ident = db.select('auth_user', where='username=$name', vars=locals())[0]
        #密码偏离值最可以通过配置定义
        if hashlib.md5("sAlT754-"+passwd).hexdigest().decode() == ident['password']:
            urls.session.login = 1
            urls.session.is_superuser = ident['is_superuser']
            #根据Dean要求追加用户名称。
            urls.session.username = name
            #render = create_render(urls.session.is_superuser)
            raise web.seeother('/home')
        else:
            urls.session.login = 0
            urls.session.is_superuser = 0
            render = create_render(urls.session.is_superuser)
            #todo 需要改成读取配置
            return render.login(msg=u'密码错误！请重新输入！')

class Reset:
    def GET(self):
        urls.session.login = 0
        urls.session.kill()
        render = create_render(urls.session.is_superuser)
        return  render.login(msg=u'请重新登录！')

