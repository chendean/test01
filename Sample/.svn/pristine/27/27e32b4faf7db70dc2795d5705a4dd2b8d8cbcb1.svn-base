#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
__author__ = 'lkx'
import web
from web.contrib.template import render_mako
from BigoCfgWeb import urls
from BigoCommon import base
import datetime

render = render_mako(
    directories=['templates'],
    input_encoding='utf-8',
    output_encoding='utf-8',
)

class task(base.WebBase):
    def get(self):
        #render画面对象
        return render.dbs_task()

    def post(self):
        pagelist=web.input()
        taskjson=self.__getTaskjson(pagelist)
        self.__save(taskjson)
        return "<script type='text/javascript'>alert('配置保存完成');window.location.href = '\home'</script>"

    def __getTaskjson(self,pagelist):
        taskjson={'jobName':'','runType':'','runOneTime':'','repeatType':'','weekDay':{},
                  'monthDay':'','startDate':'','endDate':''}
        if pagelist!=None:
            taskjson['jobName']=pagelist.jobname
            taskjson['runType']=pagelist.runType
            if pagelist.runType=='onetime':
                taskjson['runOneTime']=pagelist.runonetime

            else:
                    taskjson['repeatType']=pagelist.sel_repeat
                    taskjson['startDate']=pagelist.startD
                    taskjson['endDate']=pagelist.endD
                    if pagelist.sel_repeat=='Monthly':
                        taskjson['monthDay']=pagelist.runMonthDay
                    elif pagelist.sel_repeat=='Weekly':
                        week={}
                        if "week_Mon" in pagelist:
                            week['Monday']='Monday'
                        if "week_Tue" in pagelist:
                            week['Tuesday']='Tuesday'
                        if "week_Wes" in pagelist:
                            week['Wednesday']='Wednesday'
                        if "week_Thu" in pagelist:
                            week['Thursday']='Thursday'
                        if "week_Fri" in pagelist:
                            week['Friday']='Friday'
                        if "week_Sat" in pagelist:
                            week['Saturday']='Saturday'
                        if "week_Sun" in pagelist:
                            week['Sunday']='Sunday'
                        taskjson['weekDay']=week

        return taskjson

    def __save(self,task):
        from BigoCommon.xmlhandle import createDbs

        #2013/1/25 dean 按照review要求追加项目 displayname(显示名),description(描述),incremental(增/全量),
        # filters(增量条件),type(tble/view) ,condition(追加条件)
        #创建dbs配置文件
        #db_info{'name', 'displayname', 'serviceNamespace', 'description', 'createuser',
        # 'db'={'dbn', 'host', 'port', 'db', 'user', 'pw'},
        # 'tabledic'=[{'objname', 'incremental', 'filters', 'type', 'condition',
        # col=[{'name', 'type', 'null', 'extra'}], pk=[], index=[], param=[]}],
        # operation={}
        # }
        db_info={'name':'', 'displayname':'', 'serviceNamespace':'', 'description':'', 'createuser':'',
                'db':{}, 'tabledic':[], 'operation':{}}

        db_info['name']=urls.session.dbs['name']
        db_info['displayname']=urls.session.dbs['displayname']
        db_info['serviceNamespace']='BigO.OData.DataConnection'
        db_info['createuser']=urls.session.username
        db_info['description']=urls.session.dbs['description']
        db_info['db']=urls.session.dbs['db'].copy()
        db_info['operation']=urls.session.dbs['task'].copy()
        db_info['tabledic']=self.__gettabledic(db_info['db'])
        db_info['operation']=task

        filename='config/'+urls.session.dbs['name']+".dbs"
        createDbs(db_info,filename)

    def __gettabledic(self,dbcnn):
        from BigoCommon import sql

        userdb = self.__getcnn(dbcnn)

        query=sql.sqlquery(dbcnn['dbn'],userdb)

        tblist=urls.session.dbs['tabledic']
        tabledic=[]
        for onetb in tblist:
            tb={}
            #2013/1/25 dean 按照review要求追加项目
            # 'tabledic'=[{'objname', 'incremental', 'filters', 'type', 'sql', 'condition',
            # col=[{'name', 'type', 'null', 'extra'}], pk=[], index=[], param=[]}],
            tb={'objname':onetb['objname'], 'type':onetb['type'], 'incremental':onetb['incremental'],
                'filters':None, 'col':None, 'pk':[], 'index':None,
                'sql':onetb['sql'], 'condition':onetb['condition'], 'param':None }

            tb['filters']= onetb['filters'].split(",")
            tb['index']=query.showindex(onetb['objname'])
            tb['pk'].append({'name': "stg_id",'description':"new sys pk"})
            tb['pk'].append({'name': "stg_batch_id",'description':"new sys pk"})
            tb['col']=query.showcolinfo(onetb['objname'])
            tb['col'].append({'name': "stg_id", 'type':"BIGINT", 'length':"20", 'null':"NO",
                              'default':'AUTO_INCREMENT'})
            tb['col'].append({'name': "stg_batch_id", 'type':"BIGINT", 'length':"20", 'null':"NO"})

            tabledic.append(tb)

        return tabledic

    def __getcnn(self,dbs):
        from BigoCommon import db
        if dbs['port']=='':
            return db.database(dbn = dbs['dbn'], db = dbs['db'], user = dbs['user'],
                pw = dbs['pw'],host=dbs['host'])
        else:
            return db.database(dbn = dbs['dbn'], db = dbs['db'], user = dbs['user'],
                pw = dbs['pw'],host=dbs['host'], port=int(dbs['port']))







