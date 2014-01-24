__author__ = 'stone'
#coding=UTF-8

import pycurl
import cStringIO
import os
import time

import httplib2
import json
import urllib

buf = cStringIO.StringIO()

def getOrderTrans():
    try:
        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://180.169.94.232:8080/orderTrans/12345')
        #c.setopt(pycurl.URL,'http://localhost:8080/orderTrans/1234567')
        c.setopt(c.WRITEFUNCTION,buf.write)
        c.setopt(c.VERBOSE, True)
        c.setopt(pycurl.USERPWD,'jery:jery123')
        c.perform()

        print buf.getvalue()
        buf.close()
    except pycurl.error, error:
        errno, errstr = error
        print 'An error occurred: ', errstr

def putOrderInfoNoFile():
    try:
        btime = time.time()


        s = '[{"name":"give me a bottle of gold!"}]'

        localOrderInfo = s

        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://localhost:8080/orderInfo/623456')
        c.setopt(pycurl.HTTPHEADER,['Content-Type: application/json','Content-Length: '+str(len(localOrderInfo))])
        c.setopt(c.VERBOSE, True)
        c.setopt(pycurl.CUSTOMREQUEST,"PUT")
        c.setopt(pycurl.POSTFIELDS,localOrderInfo)
        c.setopt(c.WRITEFUNCTION,buf.write)
        c.setopt(pycurl.USERPWD,'jery:jery123')
        print "after ready curl : %f " % ((time.time() - btime),)
        c.perform()
        c.close()
        print "after do curl : %f " % ((time.time() - btime),)

        print buf.getvalue()
        buf.close()
    except pycurl.error, error:
        errno, errstr = error
        print 'An error occurred: ', errstr

def putOrderInfo():
    try:
        btime = time.time()
        filename = 'd:/I8WebServiceJson.json'
        filesize = os.path.getsize(filename)
        f = file(filename, 'rb')
        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://localhost:8080/orderInfo/12345')
        c.setopt(pycurl.PUT,1)
        c.setopt(pycurl.INFILE,f)
        c.setopt(pycurl.INFILESIZE,filesize)
        c.setopt(c.WRITEFUNCTION,buf.write)
        c.setopt(c.VERBOSE, True)
        c.setopt(pycurl.USERPWD,'jery:jery123')
        print "after ready curl : %f " % ((time.time() - btime),)
        c.perform()
        c.close()
        f.close()
        print "after do curl : %f " % ((time.time() - btime),)

        print buf.getvalue()
        buf.close()
    except pycurl.error, error:
        errno, errstr = error
        print 'An error occurred: ', errstr

def putOrderInfoHttplib2():
    h = httplib2.Http(".cache")
    h.add_credentials('jery','jery123')
    resp,content = h.request("http://localhost:8080/orderInfo/6123456","PUT",body="This is test")

if __name__ == "__main__":
    getOrderTrans()
    #putOrderInfo()
    #putOrderInfoNoFile()
    #putOrderInfoHttplib2()

