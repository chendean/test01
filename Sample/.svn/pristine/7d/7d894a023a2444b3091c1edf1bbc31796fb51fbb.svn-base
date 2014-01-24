#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
__version__ = "0.0"
__author__ = 'Dean'

import web
from web.contrib.template import render_mako
from BigoCfgWeb import urls
from BigoCommon import sql
from BigoCommon import xmlhandle
from BigoCommon import base
import json

render = render_mako(
    directories=['templates'],
    input_encoding='utf-8',
    output_encoding='utf-8',
)

#一览画面
class sqlcfg(base.WebBase):
    def get(self):
        #render画面对象
        return render.dbs_sqlcfg()

    def post(self):
        pass

#加载jqgrid
class sqlcfgload:
    def GET(self,op):

        #获取数据库连接  2013/1/23 dean
        dbsfile=""
        model=""
        if 'model' in urls.session:
            model=urls.session.model
        if 'filename' in urls.session:
            dbsfile=urls.session.filename
        #只读/复制模式
        #op=='0':grid初始化之后再提交的判断,防止copy模式下重复读取源dbs文件
        if ((model=='r') or (model=='c')) and op=='0':
            xmlreader=xmlhandle.Xmlhandle('config/'+ dbsfile)
            if (not 'dbs' in urls.session or urls.session.dbs==None):
                urls.session.dbs={'db':None, 'tabledic':None}

            if (not 'db' in urls.session.dbs or urls.session.dbs['db']==None):
                urls.session.dbs['db']=xmlreader.readDbs(piece='cfginfo')

            tabledic= xmlreader.readDbs(piece='queryinfo')

            if (not "tabledic" in urls.session.dbs or urls.session.dbs['tabledic']==None):
                urls.session.dbs['tabledic']= tabledic
            else:
                for onetb in tabledic:
                    self.__setsession(onetb['objname'], type=onetb['type'], incremental=onetb['incremental'],
                        filters=onetb['filters'], sql=onetb['sql'],
                        condition=onetb['condition'] )
            urls.session.sqlcfgloadinit=False
        #获取数据库连接  2013/1/23 dean

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

        userdb =self.__getcnn(urls.session.dbs['db'])
        rowlist=self.__getRows(userdb,filters)

        count=len(rowlist)
        #对结果集检索,排序,分页后按照jqgid默认格式返回json对象
        dic={"page":page,"total":int((count-1)/limit)+1,"records":count,
             "rows" :self.__offset(userdb,rowlist,sidx,sord,page,limit)}
        #web.header('Content-Type', 'application/json')
        return json.dumps(dic)

    #获取所有dbs文件配置信息
    #filters:查询条件[可复选]
    def __getRows(self,userdb,filters=None):

        if (not 'tabledic' in urls.session.dbs) or (urls.session.dbs['tabledic']==None):
            return []

        tabledic= urls.session.dbs['tabledic']

        for onetable in urls.session.dbs['tabledic']:
            if onetable['sql']=='':
                onetable['sql']='select * from '+onetable['objname'] + ' where 1=1'

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
                                cmpresult=self.__getfilter(onetable[field],op,data,'date')
                            else:
                                cmpresult=self.__getfilter(onetable[field],op,data)

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
                                cmpresult=self.__getfilter(onetable[field],op,data,'date')
                            else:
                                cmpresult=self.__getfilter(onetable[field],op,data)

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
    def __offset(self,userdb,dbs,sidx,sord,page,limit):
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
                colname=""
                pk=""
                query=sql.sqlquery(urls.session.dbs['db']['dbn'],userdb)
                cols=query.showcolumns(rows[i]['objname'])
                for onecol in cols:
                    if colname=="":
                        colname = onecol
                    else:
                        colname = colname + ", " + onecol

                rows[i]['col']=colname
                cols=query.showpk(rows[i]['objname'])
                for onecol in cols:
                    if pk=="":
                        pk = onecol
                    else:
                        pk = pk + ", " + onecol

                rows[i]['pk']=pk
                sqlcontent= rows[i]['sql']
                rows[i]['sql']=sqlcontent.replace('*',colname)
                #rows[i]['sql']='select %s from %s where 1=1' % (colname, rows[i]['tablename'])
                self.__setsession(rows[i]['objname'],col=colname,pk=pk,sql=rows[i]['sql'])

            i=i+1

        return rows

    #查询条件转换查询
    def __getfilter(self,cmpfrom, op, cmpto,type='string'):
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

    def __getcnn(self,dbs):
        from BigoCommon import db
        if dbs['port']=='':
            return db.database(dbn = dbs['dbn'], db = dbs['db'], user = dbs['user'],
                pw = dbs['pw'],host=dbs['host'])
        else:
            return db.database(dbn = dbs['dbn'], db = dbs['db'], user = dbs['user'],
                pw = dbs['pw'],host=dbs['host'], port=int(dbs['port']))

    def POST(self,op):
        self.op=op
        #追加条件
        if op=='1':
            #接收请求参数
            data = web.data()
            if not data=="":
                #str参数转成list
                localOrderInfos = eval(data)

            if (localOrderInfos==None) or (localOrderInfos==[]):
                pass
            else:
                self.__addcondition(localOrderInfos[0]['condition'])

        #sql check
        if op=='2':
            self.__checksql()

        #编辑
        if op=='0':
            #接收请求参数
            data = web.input()
            if (data['oper']=='edit'):
                self.__setsession(data['objname'],condition=data['condition'], filters=data['filters'])

        #应用
        if op=='3':
            #接收请求参数
            data = web.data()
            datalist = eval(data)

            if (datalist==None) or (datalist==[]):
                pass
            else:
                self.__setsession('', filters=datalist[0]['filters'], op='active')
            #if (data['oper']=='edit'):
            #    self.__setsession(data['objname'], filters=data['filters'])

    def __setsession(self,tablename,**parm):
        i=0
        op=''
        if 'op' in parm:
            op= parm['op']

        while i<len(urls.session.dbs['tabledic']):
            if op== 'active' and urls.session.dbs['tabledic'][i]['incremental']== 'true':
                if 'filters' in parm:
                    urls.session.dbs['tabledic'][i]['filters'] = parm['filters']
            else:

                if (urls.session.dbs['tabledic'][i]['objname']==tablename):

                    if 'type' in parm:
                        urls.session.dbs['tabledic'][i]['type'] = parm.pop('type')

                    if 'col' in parm:
                        urls.session.dbs['tabledic'][i]['col'] = parm.pop('col')

                    if 'incremental' in parm:
                        urls.session.dbs['tabledic'][i]['incremental'] = parm.pop('incremental')

                    if 'filters' in parm:
                        urls.session.dbs['tabledic'][i]['filters'] = parm.pop('filters')

                    if 'condition' in parm:
                        urls.session.dbs['tabledic'][i]['condition'] = parm.pop('condition')

                    if 'pk' in parm:
                        urls.session.dbs['tabledic'][i]['pk'] = parm.pop('pk')

                    if 'sql' in parm:
                        urls.session.dbs['tabledic'][i]['sql'] = parm.pop('sql')

                    return

            i=i+1

    def __addcondition(self,condition):
        if not condition=='':
            i=0
            while i<len(urls.session.dbs['tabledic']):
                urls.session.dbs['tabledic'][i]['sql']=urls.session.dbs['tabledic'][i]['sql'] + ' and ' +condition
                i=i+1

    def __checksql(self):
        errorlist=[]
        try:
            #获取当前连接
            #获取数据库连接
            userdb =self.__getcnn(urls.session.dbs['db'])
        except:
            error={}
            error={'errtype':'','errrow':''}
            error['errtype']='connection error'
            error['errrow']=''
            errorlist.append(error)
            return errorlist

        i=0
        while i<len(urls.session.dbs['tabledic']):
            urls.session.dbs['tabledic'][i]['ng']=''
            sql= 'select count(1) from ('+urls.session.dbs['tabledic'][i]['sql'] +') t'
            try:
                userdb.query(sql)
            except:
                urls.session.dbs['tabledic'][i]['ng']='ng'
                error={}
                error={'errtype':'','errrow':''}
                error['errtype']='sql error'
                error['errrow']=i
                errorlist.append(error)
            i=i+1
        return errorlist