__author__ = 'lkx'
#coding:utf-8
import os,string

#判断是否为有效目录
def IsDir(strpath):
    if os.path.isdir(strpath)== True:
        return True
    else:
        return False

#判断是否为有效文件
def isFile(strpath):
    if os.path.isfile(strpath)== True:
        return True
    else:
        return False

#判断是否为有效路径（文件或目录）
def isExists(strpath):
    if os.path.exists(strpath)== True:
        return True
    else:
        return False

#获得当前指定目录下所有文件
def getCurrFilesList(strpath):
    filelist=[]
    if isExists(strpath)== True:
        for f in os.listdir(strpath):
            if os.path.isfile(strpath + os.sep + f)==True:
                filelist.append(f)
    return filelist

#获得当前指定目录下文件名以start开始的文件
def getCurrFilesListBegin(strpath,start):
    curlist=[]
    cur=getCurrFilesList(strpath)
    for filename in cur:
        if unicode(filename).startswith(unicode(start))==True:
            curlist.append(unicode(filename))
    return curlist

#获得当前指定目录下文件名以end结尾的文件
def getCurrFilesListEnd(strpath,end):
    curlist=[]
    cur=getCurrFilesList(strpath)
    for filename in cur:
        if unicode(filename).endswith(unicode(end))==True:
            curlist.append(unicode(filename))
    return curlist

#获得当前指定目录下文件名包含strcontain的文件
def getCurrFilesListContain(strpath,strcontain):
    curlist=[]
    cur=getCurrFilesList(strpath)
    for filename in cur:
        if unicode(filename).find(unicode(strcontain))>=0:
            curlist.append(unicode(filename))
    return curlist

#获得指定目录下所有的文件
def getAllFilesList(strpath):
    list=[]
    if isExists(strpath)== True:
        for root, dir ,files in os.walk(strpath):
            for f in files:
                list.append(f)
    return list

#获得指定目录下文件名以start开始的文件
def getAllFilesListBegin(strpath,start):
    alllist=[]
    cur=getAllFilesList(strpath)
    for filename in cur:
        if unicode(filename).startswith(unicode(start))==True:
            alllist.append(unicode(filename))
    return alllist

#获得指定目录下文件名以end结尾的文件
def getAllFilesListEnd(strpath,end):
    alllist=[]
    cur=getAllFilesList(strpath)
    for filename in cur:
        if unicode(filename).endswith(unicode(end))==True:
            alllist.append(unicode(filename))
    return alllist

#获得指定目录下文件名包含strcontain的文件
def getAllFilesListContain(strpath,strcontain):
    alllist=[]
    cur=getAllFilesList(strpath)
    for filename in cur:
        if unicode(filename).find(unicode(strcontain))>=0:
            alllist.append(unicode(filename))
    return alllist
