#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
__version__ = "0.0"
__author__ = 'Dean'

from lxml import etree
from filehandle import isExists
from datetime import datetime

class Xmlhandle:

    def __init__(self, *dbsfile):
        if dbsfile == ():
            self.dbsfile=''
            pass
        else:
            self.dbsfile=dbsfile[0]



    #解析dbs配置文件取得信息块
    #piece:提取哪个信息块(cfginfo:db连接属性, tbinfo:table/view属性, queryinfo:table/view属性及其所属列
    #                    taskinfo:计划任务)
    #isinitial:初始化,仅返回空字典
    def readDbs(self, piece='', isinitial=False):

        #未指定取得片段则返回None
        if piece=='':
            return None

        try:
            #dbs_cfglist,dbs_cnncfg用
            if piece=='cfginfo':
                #2013/1/21 dean add 依据deson要求追加描述列
                returninfo={'name':'', 'createdate':'', 'updatedate':'', 'createuser':'', 'disable':'',
                                   'dbn':'', 'host': '',  'port': '', 'user': '', 'pw': '',
                                   'description': '', 'db':''}

            #dbs_tbselect or dbs_sqlcfg用
            if piece=='tbinfo' or piece=='queryinfo' :
                returninfo={'objname':'', 'type':'', 'incremental':'', 'filters':'', 'col':'', 'pk':'',
                                   'sql':'', 'condition': '',  'ng': ''}

            if piece=='taskinfo':
                returninfo={'jobName':'','runType':'','isEnable':'','runOneTime':'','repeatType':'','weekDay':{},
                            'monthDay':'','startTime':'','startDate':'','endDate':''}

            if isinitial:
                return returninfo

            #get dbs filename
            if self.dbsfile=='':
                return None
            #check file is exist
            if ( isExists(self.dbsfile)==False):
                return None

            #读取dbs配置文件
            xmlData = etree.parse(self.dbsfile)
            #dbs_cfglist,dbs_cnncfg用
            if piece=='cfginfo':
                #2013/1/21 dean add 依据deson要求追加描述列
                elemt = xmlData.getroot()
                if not (elemt==None or elemt==[]):
                    returninfo['name']= elemt.attrib['name']

                elemt = xmlData.find("//description")
                if not (elemt==None or elemt==[]):
                    returninfo['description']= elemt.text

                elemt = xmlData.find("//createdate")
                if not (elemt==None or elemt==[]):
                    returninfo['createdate']= elemt.text

                elemt = xmlData.find("//updatedate")
                if not (elemt==None or elemt==[]):
                    returninfo['updatedate']= elemt.text

                elemt = xmlData.find("//createuser")
                if not (elemt==None or elemt==[]):
                    returninfo['createuser']= elemt.text

                elemt = xmlData.find("//config")
                if not (elemt==None or elemt==[]):
                    returninfo['disable']= elemt.attrib['disable']

                #get [config]element
                cfgelemt = xmlData.findall("//config/property")

                for property in cfgelemt:
                    #get the [databaseType]
                    if (property.attrib['name'] == 'databaseType'):
                        returninfo['dbn']= property.text
                        #get the [url]
                    if (property.attrib['name'] == 'url'):
                        returninfo['host']= property.text
                        #get the [port]
                    if (property.attrib['name'] == 'port'):
                        returninfo['port']= property.text
                        #get the [databaseName]
                    if (property.attrib['name'] == 'databaseName'):
                        returninfo['db']= property.text
                        #get the [username]
                    if (property.attrib['name'] == 'username'):
                        returninfo['user']= property.text
                        #get the [password]
                    if (property.attrib['name'] == 'password'):
                        returninfo['pw']= property.text
                return returninfo

            #dbs_tbselect用
            if piece=='tbinfo' or piece=='queryinfo':

                returninfolist=[]
                #get [config]element
                queryelemts = xmlData.findall("//query")

                for property in queryelemts:
                    returninfo={}
                    returninfo={'objname':'', 'type':'', 'incremental':'', 'filters':'',
                                'col':'', 'pk':'', 'sql':'', 'condition': '',  'ng': ''}
                    #表/视图
                    returninfo['objname']= property.attrib['id']
                    returninfo['type']= property.attrib['type']
                    #增量/全量
                    returninfo['incremental']= property.attrib['incremental']

                    #dbs_sqlcfg用
                    if piece=='queryinfo':
                        returninfo['sql']= property.findtext("sql")
                        #2013/1/21 dean add 依据deson要求附加检索条件
                        elemt = property.find("condition")
                        if not (elemt==None or elemt==[]):
                            returninfo['condition']= elemt.text

                        #2013/1/21 dean add 依据deson要求追加增量条件项目
                        colelemts = property.findall("filters")
                        for col in colelemts:
                            if returninfo['filters']=="":
                                returninfo['filters']= col.attrib['name']
                            else:
                                returninfo['filters']=returninfo['filters'] + "," + col.attrib['name']

                        #列名
                        #colelemts = property.findall("//result/element")
                        #for col in colelemts:
                        #    returninfo['col'].append(col.attrib['column'])

                    returninfolist.append(returninfo)
                return returninfolist

            if piece=='taskinfo':
                #todo
                return  returninfo

        except Exception,ex:
            print ex

    #解析dbs配置文件
    #querysql={'fromtb':'', 'totb':'', 'ctbsql':'', 'query':'', 'cidsql':[],
    # 'colinfo':[{'column', 'length', 'null', 'xsdType', 'default' }]}
    def getquery(self):
        querylist=[]
        indexlist=[]
        #dbs file like infile='dbs\Karicare.dbs'
        #get dbs file content
        xmlData = etree.parse(self.dbsfile)
        #get [query]element
        querys = xmlData.findall("//query")
        for query in querys:
            #first, get the [tablename] in the "element" of the result
            result = query.find("result")
            querysql={'fromtb':query.attrib['id'], 'totb':result.attrib['element'], 'ctbsql':'',
                       'query':query.findtext("sql"), 'cidsql':[], 'colinfo':[]}

            #begin to build a create table sql
            str_CreateTable= "CREATE TABLE `%s` (" % querysql['totb']
            # then, find the element of [result] , and get all [column] and [xsdType] attribute in this data table
            cols = query.findall("result/element")
            for col in cols:
                querysql['colinfo'].append({'column':col.attrib['column'],
                                            'length':col.attrib['length'],
                                            'null':col.attrib['null'],
                                            'xsdType':col.attrib['xsdType'] })

                colnull = ''
                if(col.attrib['null']=='NO'):
                    colnull = 'NOT NULL'

                # 长度未指定的情况
                if col.attrib['length']=='' or col.attrib['length']=='0':
                    xsdType=col.attrib['xsdType'].upper()
                else:
                    xsdType=col.attrib['xsdType'].upper()+ "("+ col.attrib['length']+ ")"
                if 'default' in col.attrib:
                    defaultvalue=col.attrib['default']

                    if defaultvalue =='AUTO_INCREMENT':
                        pass
                    else:
                        if('INT' in xsdType) or ('FLOAT' in xsdType) \
                            or ('DECIMAL' in xsdType) or ('DATETIME' in xsdType)\
                            or ('TIMESTAMP' in xsdType) or ('NUMERIC' in xsdType):
                                defaultvalue="default " + defaultvalue
                        else:
                            defaultvalue="default '" + defaultvalue + "'"
                else:
                    defaultvalue=''

                #find all columns
                str_CreateTable+= ' `%s` %s %s %s ,' \
                                  % (col.attrib['column'], xsdType, colnull, defaultvalue)

            pks = query.findall("pk")
            str_pk=[]
            for pk in pks:
                str_pk.append("`%s`"%pk.attrib['name'])

            col_pk=','.join(str_pk)
            str_CreateTable += " PRIMARY KEY (%s) )" % col_pk
            str_CreateTable += ' ENGINE=InnoDB DEFAULT CHARSET=utf8'
            querysql['ctbsql']=str_CreateTable

            ids = query.findall("result/index")
            for idcol in ids:
                querysql['cidsql'].append('ALTER TABLE `%s` ADD INDEX `%s` (`%s`)'
                                  %(querysql['totb'],ids.attrib['name'],ids.attrib['key']))

            querylist.append(querysql)

        return querylist

#设置dbs有效无效属性
def enableDbs(failename, enable):
    from xml.etree.ElementTree import ElementTree

    try:
        tree = ElementTree()
        tree.parse(failename)
        p = tree.find("config")
        if (p==None):
            return False
        else:
            p.attrib['disable']=enable

        u = tree.find("updatedate")
        dt = datetime.now()
        u.text=dt.strftime( '%Y-%m-%d %H:%M:%S' )

        tree.write(failename)
        return True
    except Exception,ex:
        print ex
        return False


#2013/1/25 dean 按照review要求追加项目 displayname(显示名),description(描述),incremental(增/全量),
# filters(增量条件),type(tble/view) ,condition(追加条件)
#创建dbs配置文件
#db_info{'name', 'displayname', 'serviceNamespace', 'description', 'createuser',
# 'db'={'dbn', 'host', 'port', 'db', 'user', 'pw'},
# 'tabledic'=[{'objname', 'incremental', 'filters', 'type', 'condition', 'sql'
# col=[{'name', 'type', 'null', 'extra'}], pk=[], index=[], param=[]}],
# operation={}
# }
def createDbs(db_info, filename):
    print db_info
    #TO DO
    createtime = datetime.now()

    # Create the root element
    root_element = etree.Element('data', name=db_info['displayname'] ,
        serviceNamespace=db_info['serviceNamespace'])

    # Make a new document tree
    doc = etree.ElementTree(root_element)

    # Add the description
    description_element = etree.SubElement(root_element, 'description')
    description_element.text =db_info['description']

    # Add the createdate
    description_element = etree.SubElement(root_element, 'createdate')
    description_element.text =createtime.strftime( '%Y-%m-%d %H:%M:%S' )

    # Add the updatedate
    description_element = etree.SubElement(root_element, 'updatedate')
    description_element.text =createtime.strftime( '%Y-%m-%d %H:%M:%S' )

    # Add the createuser
    description_element = etree.SubElement(root_element, 'createuser')
    description_element.text =db_info['createuser']

    # Add the db config
    etree.Comment('db connection config')
    config_element = etree.SubElement(root_element, 'config', id=db_info['db']['db'], disable='init')
    #connection info
    property_element = etree.SubElement(config_element, 'property', name='databaseType')
    property_element.text =db_info['db']['dbn']
    property_element = etree.SubElement(config_element, 'property', name='url')
    property_element.text = db_info['db']['host']
    property_element = etree.SubElement(config_element, 'property', name='port')
    property_element.text =db_info['db']['port']
    property_element = etree.SubElement(config_element, 'property', name='databaseName')
    property_element.text =db_info['db']['db']
    property_element = etree.SubElement(config_element, 'property', name='username')
    property_element.text =db_info['db']['user']
    property_element = etree.SubElement(config_element, 'property', name='password')
    property_element.text =db_info['db']['pw']
    #query info
    etree.Comment('query config: include table structure, query sql and query params')

    for query in db_info['tabledic']:
        query_element = etree.SubElement(root_element, 'query', id=query['objname'],
            type=query['type'], incremental=query['incremental'])
        sql_element = etree.SubElement(query_element, 'sql')
        sql_element.text =query['sql']
        condition_element = etree.SubElement(query_element, 'condition')
        condition_element.text =query['condition']

        if (query['filters']==None):
            pass
        else:
            for filter in query['filters']:
                if not filter=='':
                    filter_element = etree.SubElement(query_element, 'filters')
                    filter_element.text =filter

        result_element = etree.SubElement(query_element, 'result',
                                        element=db_info['name']+'_'+query['objname'])

        if (query['col']==None):
            pass
        else:
            for column in query['col']:
                if 'default' in column:
                    element_element= etree.SubElement(result_element, 'element', column=column['name'] ,
                        xsdType=column['type'], length=column['length'],
                        null=column['null'],default=column['default'])
                else:
                    element_element= etree.SubElement(result_element, 'element', column=column['name'] ,
                        xsdType=column['type'], length=column['length'],
                        null=column['null'])

        if (query['pk']==None):
            pass
        else:
            for pk in query['pk']:
                pk_element = etree.SubElement(query_element, 'pk', name=pk['name'])

        if (query['index']==None):
            pass
        else:
            for idx in query['index']:
                idx_element = etree.SubElement(query_element, 'index', name=idx['name'], key=idx['key'])

        if (query['param']==None):
            pass
        else:
            for param in query['param']:
                param_element = etree.SubElement(query_element, 'param', name=param['name'] ,
                    ordinal =param['ordinal'], sqlType=param['sqlType'])

    #operation={'name': '', 'description':'', 'href':'', 'with-param':None}
    if (db_info['operation']==None):
        pass
    else:
        operation_element = etree.SubElement(root_element, 'operation', name='task')
        for opkey,opvalue in db_info['operation'].items():
            if type(opvalue) is dict:
                subproperty_element = etree.SubElement(operation_element, 'property',name=opkey)
                #get weekdays
                for subkey,subvalue in opvalue.items():
                    property_element = etree.SubElement(subproperty_element, 'property',name=subkey)
                    property_element.text = subvalue
            else:
                property_element = etree.SubElement(operation_element, 'property',name=opkey)
                property_element.text = opvalue




    # Save to XML file
    outFile = open(filename, 'w')
    doc.write(outFile, xml_declaration=False, encoding='utf-8',pretty_print=True)

