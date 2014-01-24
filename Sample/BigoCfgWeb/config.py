# -*- coding: utf-8 -*-
__author__ = 'Dean'
import web
from web.contrib.template import render_mako
import urls
import json

render = render_mako(
    directories=['templates'],
    input_encoding='utf-8',
    output_encoding='utf-8',
)

#一览画面
class Sql:
    def GET(self):
        #render画面对象
        return render.sqlconfig()

    def POST(self):
        pass

#加载jqgrid
class SQLLoad:
    def GET(self):
        from BigoCommon import db

        #测试代码
        if (urls.session.dbs==None):
            dbs={'db':{},'tabledic':None}
            dbinfo={'dbn':'','host':'','port':'','db':'','user':'','pw':''}
            dbinfo['dbn']='mssql'
            dbinfo['host']='192.168.0.32'
            dbinfo['port']='1433'
            dbinfo['db']='Karicare'
            dbinfo['user']='sa'
            dbinfo['pw']='!QAZ2wsxb1g0'
            dbs['db']=dbinfo

            urls.session.dbs=dbs
        #测试代码
        dbsession=urls.session.dbs['db']

        #接受jqgrid提交的请求,可设置默认值
        #ipp = web.input(rows=10,page=1,sidx='id',sord='',_search='false',searchField=None,searchOper=None,searchString=None)
        ipp=web.input()
        page = int(ipp.page)    #当前页码
        limit = int(ipp.rows)   #返回每页的记录数
        sidx= ipp.sidx          #排序主键
        if(ipp.sord=='desc'):  #排序方式(请求值与画面显示是相反的)
            sord='asc'
        else:
            sord='desc'
        search = ipp._search    #获取查询命令
        filters=None
        #查询请求为false时不可取得filters
        if (search=='true'):
            filters = eval(ipp.filters)

        #获取所有dbs
        userdb = db.database(dbn = dbsession['dbn'], db = dbsession['db'], user = dbsession['user'],
                            pw = dbsession['pw'],host=dbsession['host']+':'+dbsession['port'])
        rowlist=self._getRows(userdb,filters)

        count=len(rowlist)
        #对结果集检索,排序,分页后按照jqgid默认格式返回json对象
        dic={"page":page,"total":int((count-1)/limit)+1,"records":count,
             "rows" :self._offset(userdb,rowlist,sidx,sord,page,limit)}

        #web.header('Content-Type', 'application/json')
        return json.dumps(dic)

    #获取所有dbs文件配置信息
    #filters:查询条件[可复选]
    def _getRows(self,userdb,filters=None):

        if (urls.session.dbs['tabledic']==None):
            tables = userdb.query("SELECT name From sysobjects WHERE xtype = 'u'")

            if tables==[]:
                return []

            tobj=[]
                #读取dbs文件配置信息
            for onetable in tables:
                tabledic={'tablename':'','col':'','pk':'','sql':''}
                tabledic['tablename']=onetable['name']
                tabledic['col']=''
                tabledic['pk']=''
                tabledic['sql']='select * from '+onetable['name']
                tobj.append(tabledic)

            urls.session.dbs['tabledic']=tobj

        dbs=[]
        #读取dbs文件配置信息
        for onetable in urls.session.dbs['tabledic']:

            cmpresult=True
            #查询条件转换查询
            if not (filters==None):
                #查询关系式
                groupOp=filters['groupOp']
                #查询规则
                rules=filters['rules']
                #全部条件一致
                if (groupOp=='and') or (groupOp=='AND'):
                    cmpresult=True
                    for cmprules in rules:
                        field=cmprules['field']
                        op=cmprules['op']
                        data=cmprules['data']

                        #条件=='全部'的时候,忽略该条件
                        if(data=='all') or (data=='ALL'):
                            pass
                        else:
                            if ('date' in field):
                                cmpresult=self._getfilter(onetable[field],op,data,'date')
                            else:
                                cmpresult=self._getfilter(onetable[field],op,data)

                        #任一条件不满足则删除
                        if not cmpresult:
                            continue

                else:#任一条件满足即可
                    cmpresult=False
                    for cmprules in rules:
                        field=cmprules['field']
                        op=cmprules['op']
                        data=cmprules['data']
                        #条件=='全部'的时候,忽略该条件
                        if(data=='all') or (data=='ALL'):
                            pass
                        else:
                            if ('date' in field):
                                cmpresult=self._getfilter(onetable[field],op,data,'date')
                            else:
                                cmpresult=self._getfilter(onetable[field],op,data)

                        #任一条件满足则ok
                        if cmpresult:
                            continue
            if cmpresult:
                dbs.append(onetable)

        return dbs

    #对结果集排序,分页
    #dbs:结果集
    #sidx:排序项
    #sord:排序方式
    #page:当前页码
    #limit:每页记录数
    def _offset(self,userdb,dbs,sidx,sord,page,limit):
        from BigoCommon.utils import diclistSortasDate
        from BigoCommon.utils import diclistsort

        #排序,createdate和updatedate项目做特殊处理
        if ('date' in sidx):
            rows=diclistSortasDate(dbs,sidx,sord)
        else:
            rows=diclistsort(dbs,sidx,sord)

        #删除当前页之前所有记录
        if page>1:
            rows[0:((page-1)*limit)]=[]

        i=0
        while i<limit and i<len(rows):
            if (rows[i]['col']==''):
                str_query="SELECT FieldNo = syacol.colorder , "
                str_query+="Field = syacol.name , "
                str_query+="Iskey = CASE WHEN EXISTS ( SELECT 1 FROM sysobjects WHERE xtype = 'PK' AND parent_obj = syacol.id "
                str_query+="AND name IN ( SELECT name FROM sysindexes WHERE indid IN ( SELECT indid FROM sysindexkeys "
                str_query+="WHERE id = syacol.id AND colid = syacol.colid ))) THEN 'YES' ELSE 'NO' END "
                str_query+="FROM syscolumns syacol "
                str_query+="INNER JOIN sysobjects sysobj ON syacol.id = sysobj.id AND sysobj.xtype = 'U' AND sysobj.name <> 'dtproperties' "
                str_query+="WHERE sysobj.name =$name "
                str_query+="ORDER BY syacol.id ,syacol.colorder"

                cols = userdb.query(str_query, vars={'name':rows[i]['tablename']})
                colname=""
                pk=""
                for onecol in cols:
                    if colname=="":
                        colname = onecol['Field']
                    else:
                        colname = colname + ", " + onecol['Field']

                    if onecol['Iskey']=="YES":
                        if pk=="":
                            pk = onecol['Field']
                        else:
                            pk = pk + ", " + onecol['Field']

                rows[i]['col']=colname
                rows[i]['pk']=pk
                rows[i]['sql']='select %s from %s' % (colname, rows[i]['tablename'])

                self._setsession(rows[i]['tablename'],col=colname,pk=pk,sql=rows[i]['sql'])

            i=i+1

        return rows

    #查询条件转换查询
    def _getfilter(self,cmpfrom, op, cmpto,type='string'):
        from BigoCommon.utils import cmp_datetime
        #等于
        if op=='eq':
            if (type=='string') or (type=='num'):
                return cmpfrom==cmpto

            if (type=='date'):
                if cmp_datetime(cmpfrom,cmpto,'%Y-%m-%d')==0:
                    return True

        #不等于
        if op=='ne':
            if (type=='string') or (type=='num'):
                return cmpfrom==cmpto

            if (type=='date'):
                if not cmp_datetime(cmpfrom,cmpto,'%Y-%m-%d')==0:
                    return True
            #小于
        if op=='lt':
            if (type=='string') or (type=='num'):
                return cmpfrom<cmpto

            if (type=='date'):
                if cmp_datetime(cmpfrom,cmpto,'%Y-%m-%d')==1:
                    return True
            #大于
        if op=='gt':
            if (type=='string') or (type=='num'):
                return cmpfrom>cmpto

            if (type=='date'):
                if cmp_datetime(cmpfrom,cmpto,'%Y-%m-%d')==-1:
                    return True
            #小于等于
        if op=='le':
            if (type=='string') or (type=='num'):
                return cmpfrom<=cmpto

            if (type=='date'):
                if not cmp_datetime(cmpfrom,cmpto,'%Y-%m-%d')==-1:
                    return True

        #大于等于
        if op=='ge':
            if (type=='string') or (type=='num'):
                return cmpto<=cmpfrom

            if (type=='date'):
                if not cmp_datetime(cmpfrom,cmpto,'%Y-%m-%d')==1:
                    return True

        return False

    def POST(self):
        #接收请求参数
        data = web.input()

        if (data['oper']=='edit'):

            self._setsession(data['tablename'],sql=data['sql'])


    def _setsession(self,tablename,**parm):
        i=0
        while i<len(urls.session.dbs['tabledic']):

            if (urls.session.dbs['tabledic'][i]['tablename']==tablename):

                if 'col' in parm:
                    urls.session.dbs['tabledic'][i]['col'] = parm.pop('col')

                if 'pk' in parm:
                    urls.session.dbs['tabledic'][i]['pk'] = parm.pop('pk')

                if 'sql' in parm:
                    urls.session.dbs['tabledic'][i]['sql'] = parm.pop('sql')

                return

            i=i+1
