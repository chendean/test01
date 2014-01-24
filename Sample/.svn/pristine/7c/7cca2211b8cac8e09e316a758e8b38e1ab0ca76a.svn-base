__author__ = 'leon'
#coding:utf-8

import web
#Session模式不能debug
#web.config.debug = False

urls = (
    '/', 'login.Login',
    '/login', 'login.Login',
    '/reset', 'login.Reset',
    '/home', 'home.home',
    '/dbs_cfglist', 'dbs.dbs_cfglist.cfglist',
    '/dbs_cfgload/(\d+)', 'dbs.dbs_cfglist.cfgload',
    '/dbs_sqlcfg', 'dbs.dbs_sqlcfg.sqlcfg',
    '/dbs_sqlcfgload/(\d+)', 'dbs.dbs_sqlcfg.sqlcfgload',
    '/dbs_task', 'dbs.dbs_task.task',
    '/dbs_cnncfg', 'dbs.dbs_cnncfg.cnncfg',
    '/dbs_tbselect','dbs.dbs_tbselect.tbselect',
    '/dbs_tbselect/gettable','dbs.dbs_tbselect.gettable',
    '/dbs_tbincremental','dbs.dbs_tbincremental.tbincremental',
    '/dbs_tbincremental/gettable','dbs.dbs_tbincremental.gettable',

    '/etl_stgselect','etl.etl_stgselect.stgselect',
    '/etl_stgLoad/(\d+)','etl.etl_stgselect.stgLoad'
)

app = web.application(urls, locals())

#Session模式调试用，正式发布必须注销，用下面的session方式。不然会导致使用相同的session
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'),
        {'login': 0, 'is_superuser': 0, 'username': ''})
    web.config._session = session
else:
    session = web.config._session

#在正式发布或者不需要调试模式下，请打开下面这段代码
'''
store = web.session.DiskStore('sessions')
session = web.session.Session(app, store,
    initializer={'login': 0, 'is_superuser': 0})
'''

if __name__ == "__main__":
    app.run()



