# -*- coding: utf-8 -*-
__author__ = 'Dean'
import web
from web.contrib.template import render_mako
import json

render = render_mako(
    directories=['templates'],
    input_encoding='utf-8',
    output_encoding='utf-8',
)

#一览画面
class View:
    def GET(self):
        #render画面对象
        return render.view()

    def POST(self):
        pass

#加载jqgrid
class Load:
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

        #获取所有dbs
        rowlist=self._getRows(filters)
        count=len(rowlist)
        #对结果集检索,排序,分页后按照jqgid默认格式返回json对象
        dic={"page":page,"total":int((count-1)/limit)+1,"records":count,
             "rows" :self._offset(rowlist,sidx,sord,page,limit)}
        #web.header('Content-Type', 'application/json')
        return json.dumps(dic)

    #获取所有dbs文件配置信息
    #filters:查询条件[可复选]
    def _getRows(self,filters=None):
       from BigoCommon.xmlhandle import Xmlhandle
       from BigoCommon.filehandle import getCurrFilesListEnd

       #获取所有dbs文件
       filelist=getCurrFilesListEnd('config','dbs')

       dbs=[]
       #读取dbs文件配置信息
       for onefile in filelist:
           xmlreader=Xmlhandle('config/'+ onefile)
           namedic={'name':onefile.encode('utf-8')}
           dbsdic=xmlreader.getDbsConfig()
           dbsdic.update(namedic)
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
                               cmpresult=self._getfilter(dbsdic[field],op,data,'date')
                           else:
                               cmpresult=self._getfilter(dbsdic[field],op,data)

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
                               cmpresult=self._getfilter(dbsdic[field],op,data,'date')
                           else:
                               cmpresult=self._getfilter(dbsdic[field],op,data)

                       #任一条件满足则ok
                       if cmpresult:
                           continue
           if cmpresult:
                dbs.append(dbsdic)

       return dbs

    #对结果集排序,分页
    #dbs:结果集
    #sidx:排序项
    #sord:排序方式
    #page:当前页码
    #limit:每页记录数
    def _offset(self,dbs,sidx,sord,page,limit):
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

    def POST(self,op):
        from BigoCommon.xmlhandle import enableDbs
        #接收请求参数
        data = web.data()

        if not data=="":

            #str参数转成list
            localOrderInfos = eval(data)

            if (localOrderInfos==None) or (localOrderInfos==[]):
                pass
            else:
                for orderinfo in localOrderInfos:
                    #无效
                    if op=='1':
                        if (orderinfo['val']=='true'):
                            enableDbs('config/'+ orderinfo['name'],'false')
                        else:
                            enableDbs('config/'+ orderinfo['name'],'true')
                    #删除
                    if op=='2':
                        pass
