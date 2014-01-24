#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
__version__ = "0.0"
__author__ = 'Mkk'

import web
from web.contrib.template import render_mako
from BigoCfgWeb import urls
from BigoCommon import sql
from BigoCommon import confighandle
from BigoCommon import base
import json

render = render_mako(
    directories=['templates'],
    input_encoding='utf-8',
    output_encoding='utf-8',
)

class cnncfg(base.WebBase):
    def get(self):
        dbs = {'name':"", 'displayname':"", 'description':"", 'db':{},'tabledic':[],'task':{}}
        urls.session.dbs = dbs
        conf= confighandle.DBConfigInfo()
        ports=conf.getDBParameters('db_default_port')
        return render.dbs_cnncfg()
    def post(self):
        i=web.input()
        test = self.testConnection(i)
        if(len(test)<>0):
            urls.session.dbs['name']= i.pop('name')
            urls.session.dbs['displayname'] = i.pop('displayname')
            urls.session.dbs['description'] = i.pop('description')
            urls.session.dbs['db'] = i
            return test
        else:
            return 'false'

    def testConnection(self,cnn):
        from BigoCommon import db
        from BigoCommon.filehandle import getCurrFilesListEnd

        #获取所有dbs文件
        filelist=getCurrFilesListEnd('config','dbs')
       # print filelist
        if (str(cnn['name'])+'.dbs' in filelist):

            return Exception('配置文件"'+str(cnn['name'])+'.dbs'+'"已存在')

        try:
            dblist={}
            userdb = db.database(dbn = cnn['dbn'], db = cnn['db'], user = cnn['user'],
            pw = cnn['pw'],host = cnn['host'] ,port = int(cnn['port']))
            dbquery = sql.sqlquery(cnn['dbn'],userdb)
            dblist=dbquery.showschema()
            for item in dblist:
                 item['Database']=item['Database'].encode('utf-8')
            dbquery=None
            userdb = None
        except Exception,ex:
            print ex
            return  {}
        else:
            return dblist
