#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
__version__ = "0.0"
__author__ = 'Dean'
from BigoCommon import confighandle

class sqlquery:

    def __init__(self, type, dbcnn):
        self.type=type
        self.dbcnn=dbcnn

    #返回获得的数据列表
    def showschema(self):
        DBdict={}
        if not self.__checkparm(type=self.type, dbcnn=self.dbcnn):
            return DBdict
        if self.type=='mysql':
            self.dbcnn.keywords['db']='mysql'
            DBdict=self.dbcnn.query("show databases " )
            return DBdict
        if self.type=='mssql':
            conf=confighandle.DBConfigInfo()
            where=conf.getDBParameterValueString('get_database_list','sqlserver_where')
            DBdict=self.dbcnn.query("SELECT name 'Database' FROM master..sysdatabases WHERE dbid not in (%s) " % where )
            return DBdict

        if self.type=='oracle':
            return DBdict

        return DBdict
    #查找所有表
    def showtables(self):
        if not self.__checkparm(type=self.type, dbcnn=self.dbcnn):
            return []

        if self.type=='mysql':
            #tables = self.dbcnn.query("show tables")
            tables = self.dbcnn.query("SELECT table_name text FROM information_schema.tables where TABLE_SCHEMA ='" + self.dbcnn.keywords["db"] + "'")

        if self.type=='mssql':
            tables = self.dbcnn.query("SELECT name text From sysobjects WHERE xtype = 'u'")

        if self.type=='oracle':
            tables = self.dbcnn.query("SELECT table_name text From user_tables")

        return tables

    #查找所有表
    def showviews(self):
        if not self.__checkparm(type=self.type, dbcnn=self.dbcnn):
            return []

        if self.type=='mysql':
            #tables = self.dbcnn.query("show tables")
            tables = self.dbcnn.query("SELECT table_name text FROM information_schema.tables where TABLE_SCHEMA ='" + self.dbcnn.keywords["db"] + "'")

        if self.type=='mssql':
            tables = self.dbcnn.query("SELECT name text From sysobjects WHERE xtype = 'v'")

        if self.type=='oracle':
            tables = self.dbcnn.query("SELECT table_name text From user_views")

        return tables

    #查找表中所有列
    def showcolumns(self,tbname):
        if not self.__checkparm(type=self.type, dbcnn=self.dbcnn, tbname=tbname):
            return []

        if self.type=='mysql':
            columns = self.dbcnn.query('desc %s' % tbname)

        if self.type=='mssql':
            str_query="SELECT Field = syacol.name "
            str_query+="FROM syscolumns syacol "
            str_query+="INNER JOIN sysobjects sysobj ON syacol.id = sysobj.id AND " \
                       "(sysobj.xtype = 'U' OR sysobj.xtype = 'V') AND sysobj.name <> 'dtproperties' "
            str_query+="WHERE sysobj.name =$name "
            str_query+="ORDER BY syacol.id ,syacol.colorder"
            columns = self.dbcnn.query(str_query, vars={'name':tbname})

        if self.type=='oracle':
            columns = self.dbcnn.query('desc %s' % tbname)

        if columns==[]:
            return []

        returnlist=[]
        for onecol in columns:
            returnlist.append(onecol['Field'])

        return returnlist

    #查找表中所有主键
    def showpk(self,tbname):
        if not self.__checkparm(type=self.type, dbcnn=self.dbcnn, tbname=tbname):
            return None

        returnlist=[]
        if self.type=='mysql':
            pks = self.dbcnn.query('desc %s' % tbname)
            if pks==[]:
                return []
            for onecol in pks:
                if(onecol['Key']=='PRI'):
                    returnlist.append(onecol['Field'])

        if self.type=='mssql':
            pks = self.dbcnn.query("sp_pkeys '%s'" % tbname)
            if pks==[]:
                return []
            for onecol in pks:
                returnlist.append(onecol['COLUMN_NAME'])

        if self.type=='oracle':
            pks = self.dbcnn.query('desc %s' % tbname)
            if pks==[]:
                return []
            for onecol in pks:
                if(onecol['Key']=='PRI'):
                    returnlist.append(onecol['Field'])

        return returnlist

    #check表是否存在
    def checktableexits(self, tbname):
        if not self.__checkparm(type=self.type, dbcnn=self.dbcnn, tbname=tbname):
            return False

        if self.type=='mysql':
            tables = self.dbcnn.query("show tables like '%s'" % tbname)
            if tables==[]:
                return False
            else:
                return True

        if self.type=='mssql':
            tables = self.dbcnn.query("SELECT count(1) AS ret From sysobjects WHERE name = '%s'" % tbname)

        if self.type=='oracle':
            tables = self.dbcnn.query("SELECT count(1) AS ret From user_tables WHERE table_name = '%s'" % tbname)

        if tables==[]:
            return False

        if tables[0]['ret']>0:
            return True

        return False

    #查找表中所有索引
    def showindex(self,tbname):
        returnlist=[]
        try:

            if not self.__checkparm(type=self.type, dbcnn=self.dbcnn, tbname=tbname):
                return []


            if self.type=='mysql':
                ids = self.dbcnn.query('show index from %s' % tbname)
                if ids==[]:
                    return []
                for onecol in ids:
                    oneid={}
                    oneid={'name':onecol['Key_name'], 'key':onecol['Column_name']}
                    returnlist.append(oneid)

            if self.type=='mssql':
                ids = self.dbcnn.query('sp_helpindex [%s]' % tbname)
                if ids==[] or ids==-1:
                    return []

                for onecol in ids:
                    oneid={}
                    oneid={'name':onecol['index_name'], 'key':onecol['index_keys']}
                    returnlist.append(oneid)

            if self.type=='oracle':
                ids = self.dbcnn.query('show index from %s' % tbname)
                if ids==[]:
                    return []
                for onecol in ids:
                    oneid={}
                    oneid={'name':onecol['Key_name'], 'key':onecol['Column_name']}
                    returnlist.append(oneid)
            return returnlist
        except Exception,ex:
            print ex
        finally:
            return returnlist

    #查找表中所有列
    def showcolinfo(self,tbname):
        if not self.__checkparm(type=self.type, dbcnn=self.dbcnn, tbname=tbname):
            return []

        #col={'name':'', 'type':'', 'length':'', 'null':'', 'default':''}
        if self.type=='mysql':
            columns = self.dbcnn.query('desc %s' % tbname)
            if columns==[]:
                return []

            returnlist=[]
            for onecol in columns:
                returnlist.append({'name':onecol['Field'],
                                   'type':onecol['Type'],
                                   'length':"",
                                   'null':onecol['Null']}
                )

        if self.type=='mssql':

            str_query="SELECT FieldNo = syacol.colorder , "
            str_query+="Field = syacol.name , "
            str_query+="Type = coltype.name ,"
            str_query+="Bits = syacol.length ,"
            str_query+="Length = COLUMNPROPERTY(syacol.id, syacol.name, 'PRECISION') ,"
            str_query+="Decimal = ISNULL(COLUMNPROPERTY(syacol.id, syacol.name, 'Scale'), 0) ,"
            str_query+="Isnull = CASE WHEN syacol.isnullable = 1 THEN 'YES' ELSE 'NO' END, "
            str_query+="Defvalue = ISNULL(syscmt.text, '')"
            str_query+="FROM syscolumns syacol "
            str_query+="LEFT JOIN systypes coltype ON syacol.xusertype = coltype.xusertype "
            str_query+="INNER JOIN sysobjects sysobj ON syacol.id = sysobj.id AND " \
                       "(sysobj.xtype = 'U' OR sysobj.xtype = 'V') AND sysobj.name <> 'dtproperties' "
            str_query+="LEFT JOIN syscomments syscmt ON syacol.cdefault = syscmt.id "
            str_query+="WHERE sysobj.name =$name "
            str_query+="ORDER BY syacol.id ,syacol.colorder"

            columns = self.dbcnn.query(str_query, vars={'name':tbname})

            if columns==[]:
                return []

            #fix mysql createtable issure
            #OperationalError: (1118, 'Row size too large. The maximum row size for the used table type,
            # not counting BLOBs, is 65535. You have to change some columns to TEXT or BLOBs')
            maxsize=65532
            rowsize=0
            colindex=0
            colindex_lastchar=0
            returnlist=[]
            for onecol in columns:
                #coltype格式:['formattype','formatlength:(Length,Decimal)']
                coltype=typemapping(self.type,onecol['Type'],onecol['Length'],onecol['Decimal'])
                returnlist.append({'name':onecol['Field'],
                                   'type':coltype[0],
                                   'length':coltype[1],
                                   'null':onecol['Isnull']}
                )
                #utf8格式的CHAR与VARCHAR单个字符长度需乘以3

                if ('CHAR' in coltype[0]):
                    rowsize=rowsize+ int(coltype[1])*3
                    colindex_lastchar=colindex
                else:
                    if ('TEXT' in coltype[0]) or ('BLOB' in coltype[0]):
                        pass
                    else:
                        rowsize=rowsize+onecol['Length']
                #单行总长超过最大值时，按照mysql的提示要求，将直近的CHAR或VARCHAR列改为BLOB类型
                if rowsize>maxsize:
                    returnlist[colindex_lastchar]['type']="BLOB"

                colindex=colindex+1

        if self.type=='oracle':
            columns = self.dbcnn.query('desc %s' % tbname)
            if columns==[]:
                return []

            returnlist=[]
            for onecol in columns:
                returnlist.append({'name':onecol['Field'],
                                   'type':onecol['Type'],
                                   'length':"",
                                   'null':onecol['Null']}
            )

        return returnlist

    def __checkparm(self,**keywords):
        if 'type' in keywords:
            if keywords.pop('type')=='':
                return False

        if 'dbcnn' in keywords:
            if keywords.pop('dbcnn')==None:
                return False

        if 'tbname' in keywords:
            if keywords.pop('tbname')=='':
                return False

        return True

#数据库字段类型转换(mssql->mysql , oracle->mysql)
#type:字段类型
#length:字段长度
#fromdb:对象数据库
#todb:目标数据库(mysql)
def typemapping(fromdb,type,length,decimal=0,todb='mysql'):
    #未指定type则返回空
    if type=='':
        return ['','']
    #未指定数据库类型或者目标数据库与对象数据库同类型，则原type返回
    if fromdb=='' or todb=='' or fromdb==todb:
        formattype=type.upper()
        if 'TIME' in formattype or 'DATE' in formattype:
            return [formattype,'']
        if length>0:
            formatlength='%d'% length
        if decimal>0:
            formatlength+=',%d'% decimal

        return [formattype, formatlength]

    if fromdb=='mssql':

        if todb=='mysql':
            type=type.upper()
            if (type=='CHAR' or type=='BINARY' or type=='VARBINARY' or  type=='IMAGE'):
                #length==-1 等同于对象DB该类型MAXLENGTH
                if length>255 or length==-1:
                    type=type+'>255'

            if (type=='NCHAR' or type=='VARCHAR' or type=='NVARCHAR'
                or type=='TEXT' or  type=='NTEXT'):
                if length>4294967295:
                    type=type+'>4294967295'

                #length==-1 等同于对象DB该类型MAXLENGTH
                if length>65535 or length==-1:
                    type=type+'>65535'

            formattype= mssql_mysql_type_dic[type]

    if fromdb=='oracle':
        if todb=='mysql':
            type=type.upper()
            if (type=='VARCHAR' or type=='VARCHAR2' or type=='VARCHAR'
            or type=='CHAR' or  type=='LONG' or  type=='LONGRAW' or  type=='RAW'):
                #length==-1 等同于对象DB该类型MAXLENGTH
                if length>255 or length==-1:
                    type=type+'>255'
            formattype= oracle_mysql_type_dic[type]

    if '#' in formattype:
        return [formattype.split('#')[0], formattype.split('#')[1]]
    else:
        formatlength=''
        if 'TIME' in formattype or 'DATE' in formattype:
            return [formattype,formatlength]
        if length>0:
            formatlength='%d'% length
        if decimal>0:
            formatlength+=',%d'% decimal

        return [formattype,formatlength]

mssql_mysql_type_dic={
    'INT':'INT',
    'TINYINT':'TINYINT',
    'SMALLINT':'SMALLINT',
    'BIGINT':'BIGINT',
    'BIT':'TINYINT#1',
    'FLOAT':'FLOAT',
    'REAL':'FLOAT',
    'NUMERIC':'DECIMAL',
    'DECIMAL':'DECIMAL',
    'MONEY':'DECIMAL',
    'SMALLMONEY':'DECIMAL',
    'CHAR':'CHAR',
    'CHAR>255':'TEXT',
    'NCHAR':'CHAR',
    'NCHAR>65535':'TEXT',
    'NCHAR>4294967295':'LONGTEXT#0',
    'VARCHAR':'VARCHAR',
    'VARCHAR>65535':'TEXT',
    'VARCHAR>4294967295':'LONGTEXT#0',
    'NVARCHAR':'VARCHAR',
    'NVARCHAR>65535':'TEXT',
    'NVARCHAR>4294967295':'LONGTEXT#0',
    'DATE':'DATE',
    'DATETIME':'DATETIME',
    'DATETIME2':'DATETIME',
    'SMALLDATETIME':'DATETIME',
    'DATETIMEOFFSET':'DATETIME',
    'TIME':'TIME',
    'TIMESTAMP':'TIMESTAMP',
    'ROWVERSION':'TIMESTAMP',
    'BINARY':'BLOB',
    'BINARY>255':'LONGBLOB#0',
    'VARBINARY':'VARBINARY',
    'VARBINARY>255':'LONGBLOB#0',
    'TEXT':'VARCHAR',
    'TEXT>65535':'TEXT',
    'TEXT>4294967295':'LONGTEXT#0',
    'NTEXT':'VARCHAR',
    'NTEXT>65535':'TEXT',
    'NTEXT>4294967295':'LONGTEXT#0',
    'IMAGE':'TINYBLOB',
    'IMAGE>255':'LONGBLOB#0',
    'SQL_VARIANT':'LONGBLOB#0', #not migrated type
    'TABLE':'LONGBLOB#0',#not migrated type
    'HIERARCHYID':'LONGBLOB#0',#not migrated type
    'UNIQUEIDENTIFIER':'VARCHAR#64',
    'SYSNAME':'VARCHAR#160',
    'XML':'TEXT'
}

oracle_mysql_type_dic={
    'NUMBER':'NUMERIC',
    'DEC':'NUMERIC',
    'DECIMAL':'NUMERIC',
    'NUMERIC':'NUMERIC',
    'DOUBLE PRECISION':'NUMERIC',
    'FLOAT':'NUMERIC',
    'REAL':'NUMERIC',
    'SMALLINT':'SMALLINT',
    'VARCHAR':'VARCHAR',
    'VARCHAR2':'VARCHAR',
    'CHAR':'CHAR',
    'VARCHAR2>255':'TEXT',
    'VARCHAR>255':'TEXT',
    'CHAR>255':'TEXT',
    'LONG':'VARCHAR',
    'LONGRAW':'VARCHAR',
    'RAW':'VARCHAR',
    'LONG>255':'TEXT',
    'LONGRAW>255':'TEXT',
    'RAW>255 ':'TEXT',
    'DATE':'DATETIME'
    }

def getseqcurrval(dbcnn,seqname):
    querystr="select currval('"+ seqname +"')";
    result=dbcnn.query(querystr)
    for row in result:
        for key in row:
            return row[key]

def getseqnextval(dbcnn,seqname):
    querystr="select nextval('"+ seqname +"')";
    result=dbcnn.query(querystr)
    for row in result:
        for key in row:
            return row[key]

def resetseq(dbcnn, seqname, seqval):
    querystr="select setval('%s', %d)" % (seqname, seqval);
    result=dbcnn.query(querystr)
    for row in result:
        for key in row:
            return row[key]