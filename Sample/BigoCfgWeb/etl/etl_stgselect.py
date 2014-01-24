#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
__version__ = "0.0"
__author__ = 'ZK'

import web
import pymssql
from web.contrib.template import render_mako
from BigoCfgWeb import urls
from BigoCommon import sql
from BigoCommon import confighandle
from BigoCommon import base

import BigoCommon.db
import json

render = render_mako(
    directories=['templates'],
    input_encoding='utf-8',
    output_encoding='utf-8',
)

db = BigoCommon.db.database(dbn='sqlite', db='db\BigoCfgDb.db')
class stgselect(base.WebBase):
    def get(self):
        #页面显示
        return render.etl_stgselect()

    def post(self):
        pass
class stgLoad:
    def GET(self,op):
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
        #获取所有的数据库信息
        reslist=self.__getRows(filter)
        count=len(reslist)
        #对结果集检索,排序,分页后按照jqgid默认格式返回json对象
        dic={"page":page,"total":int((count-1)/limit)+1,"records":count,
             "rows" :self.__offset(reslist,sidx,sord,page,limit)}
        #web.header('Content-Type', 'application/json')
        print dic
        return json.dumps(dic)

    #filters:查询条件查找BigoSC中所有的数据信息
    def __getRows(self,filters=None):
        from BigoCommon import db
        userdb = db.database(dbn = 'mssql', db = 'BigoSC', user = 'sa',pw = '!QAZ2wsxb1g0',host='192.168.0.32',port=1433)
        result = userdb.query("select SchemaName,createbyid,SchemaId,ConfigStatus,convert(date,CreateDate) CreateDate,UpdateById,convert(date,UpdateDate)UpdateDate from DBS_SYS_SCHEMA; ")
        return result

    #对结果集排序,分页
        #dbs:结果集
        #sidx:排序项
        #sord:排序方式
        #page:当前页码
        #limit:每页记录数
    def __offset(self,dbs,sidx,sord,page,limit):
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

        return rows



    def POST(self,op):
        from BigoCfgWeb import urls
        from BigoCommon.xmlhandle import enableDbs
        #下一步事件
        if op=="1":
          pass


