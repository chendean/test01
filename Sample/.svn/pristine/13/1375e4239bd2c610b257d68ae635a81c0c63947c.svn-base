#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
__author__ = 'Dean'
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from BigoCommon.xmlhandle import Xmlhandle
from BigoCommon import db
from BigoCommon import sql
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
    '/(.*)', 'dataload'
    )
app = web.application(urls, globals())

class dataload:
    @ds(
        default = 'xml',
        html = render_html,
        xml  = render_xml,
        json = render_json,
        txt  = render_txt
    )
    def GET(self, name):

        return ''

    def POST(self, name):
        '''data = web.data()
    localOrderInfos = json.loads(data)
'''
        self.__loaddata()
        return {'message': 'done'}

    def __convertnone(self, obj):
        if obj==None :
            return "NULL"
        else:
            return obj

    def __convertvalue(self, value, type):
        convalue = self.__convertnone(value)
        if convalue=="NULL":
            return convalue
        if ("INT" in type) or ("FLOAT" in type)  or ("DECIMAL" in type)\
        or ("NUMERIC" in type) :
            return str(convalue)
        if ("TIME" in type):
            return "'" + str(convalue) + "'"

        if ("'" in str(convalue)):
            return "'" + str(convalue).replace("'","''") + "'"
        else:
            return "'" + str(convalue)+ "'"

    def __getcnn(self, dbs):
        if dbs['port']=='':
            return db.database(dbn = dbs['dbn'], db = dbs['db'], user = dbs['user'],
                pw = dbs['pw'],host=dbs['host'], charset="utf8")
        else:
            return db.database(dbn = dbs['dbn'], db = dbs['db'], user = dbs['user'],
                pw = dbs['pw'],host=dbs['host'], port=int(dbs['port']),charset="utf8")

    def __getbatchid(self, dbcnn):
        querystr="select max(batch_id) as maxid from stg_log"
        result=dbcnn.query(querystr)
        if result==None or []:
            return 0

        if result[0]['maxid']==None or result[0]['maxid']=='NULL':
            return 0

        return result[0]['maxid']

    def __insertStglog(self, dbcnn, id, batchid, source, fromtb, totb):
        querystr="insert into stg_log (id, batch_id, create_time, update_time, "\
                 "create_user, update_user, upload_status, upload_source, upload_table_from, "\
                 "upload_table_to, upload_row_count, upload_begin_time, upload_end_time ) "\
                 "values( %d, %d, NULL, NULL, '%s', NULL, '%s' , '%s' , '%s' , '%s' , 0, "\
                 "CURRENT_TIMESTAMP, NULL)" %(id, batchid, "dbs", "begin", source, fromtb, totb)

        dbcnn.query(querystr)

    def __updateStglog(self, dbcnn, stglogid, rowcount):
        querystr="update stg_log set update_time=CURRENT_TIMESTAMP, update_user='%s', "\
                 "upload_status='%s', upload_row_count=%d, upload_end_time=CURRENT_TIMESTAMP "\
                 "where id=%d " % ("dbs", "done", rowcount, stglogid)
        dbcnn.query(querystr)

    def __loaddata(self):
        dbshandle=Xmlhandle('../../BigoCfgWeb/config/newkaricare.dbs')
        targetdbinfo=dbshandle.getDbsConfig(True)
        sqllist=dbshandle.getquery()
        targetdb=self.__getcnn(targetdbinfo)

        dbs={}
        dbs['dbn']='mysql'
        dbs['db']='test'
        dbs['user']='leon'
        dbs['pw']='zaq12wsx'
        dbs['host']='192.168.0.32'
        dbs['port']=3306

        sysdb=self.__getcnn(dbs)
        sqlquery=sql.sqlquery(dbs['dbn'], sysdb)
        batchid =self.__getbatchid(sysdb)

        for onesql in sqllist:

            try:
                sysdbtran = sysdb.transaction()

                if not sqlquery.checktableexits(onesql['totb']):
                    print onesql['ctbsql']
                    sysdb.query(onesql['ctbsql'])

                print onesql['totb']
                #querystr='drop table ' + onesql['totb']
                #queryresult=sysdb.query(querystr)
                #insertsql= "TRUNCATE TABLE " + onesql['totb']
                #print insertsql
                #sysdb.query(insertsql)
                stglogid= sql.getseqnextval(sysdb, 'stglogseq')
                self.__insertStglog(sysdb, stglogid, int(batchid)+1, targetdbinfo['host']+ ":"+ targetdbinfo['db'],
                    onesql['fromtb'], onesql['totb'])

                querystr='select top 2000000 * from ( '+ onesql['query'] + ') tb'
                queryresult=targetdb.query(querystr)
                for row in queryresult:
                    columns="`stg_id`, `stg_batch_id`"
                    values="NULL, %d" % (batchid+1)
                    for key in row:

                        for itemdic in  onesql['colinfo']:
                            if itemdic['column']==key:
                                columns+=", `" + key + "`"
                                values+=", " + self.__convertvalue(row[key], itemdic['xsdType'])

                    insertsql= "insert into %s (%s) values (%s)" % (onesql['totb'], columns, values)

                    sysdb.query(insertsql)

                self.__updateStglog(sysdb, stglogid, len(queryresult))

            except:
                sysdbtran.rollback()
                raise
            else:
                sysdbtran.commit()

if __name__ == "__main__":
    app.run()







