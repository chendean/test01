__author__ = 'lkx'
#coding:utf-8
import ConfigParser
import string, os, sys

#获取DB配置所所需的参数：dbhost、dbname 等
class DBConfigInfo():
    __configfile="config/web.conf"
    __cf=ConfigParser.ConfigParser()

    #类初始化：获取DB配置文件
    def __init__(self):
        self.__cf.read(self.__configfile)

    #获得DB配置文件的所有DB信息
    def getAllDB(self):
        return self.__cf.sections()

    #获取DB配置文件中指定DB下所有信息
    def getDBParameters(self,sectionkey):
        return self.__cf.options(sectionkey)

    #获得DB配置文件中指定DB某个参数的value（string）
    def getDBParameterValueString(self,sectionkey,itemkey):
        return self.__cf.get(sectionkey,itemkey)

    #获得DB配置文件中指定DB某个参数的value（int）
    def getDBParameterValueInt(self,sectionkey,itemkey):
        return self.__cf.getint(sectionkey,itemkey)

#获得Message 信息
class MessageInfo():
    __configfile="MessageConfigFile.conf"
    __cf=ConfigParser.ConfigParser()

    #类初始化：获取MSG配置文件
    def __init__(self):
        self.__cf.read(self.__configfile)

    #获得MSG配置文件的所有MSG分类信息
    def getAllMsgType(self):
        return self.__cf.sections()

    #获取MSG配置文件中指定MSG type下所有信息
    def getMsgKeyCode(self,sectionkey):
        return self.__cf.options(sectionkey)

    #获得MSG配置文件中指定MSG type某个keycode 对应的的info（string）
    def getMsgString(self,sectionkey,itemkey):
        return self.__cf.get(sectionkey,itemkey)

