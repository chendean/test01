__author__ = 'leon'
#coding:utf-8

import pycurl
import cStringIO
import os
import time
import httplib2
import json
import urllib

buf = cStringIO.StringIO()
# simple
pf = {'name': 'value1'}
def getvalue():
    try:
        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8080/fadsfadfa')
        c.setopt(pycurl.HTTPGET,1)
        c.setopt(c.WRITEFUNCTION, buf.write)
        c.setopt(c.VERBOSE, True)

        c.perform()
        c.close()
        print buf.getvalue()
        buf.close()
        print("it's over")
    except pycurl.error, error:
        errno, errstr = error
        print 'An error occurred: ', errstr

#getvalue()

def getPostvalue():
    try:
        s = '[{"name":"give me a bottle of gold!"}]'
        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8080/fadsfadfa')
        c.setopt(pycurl.HTTPHEADER,['Content-Type: application/json','Content-Length: '+str(len(s))])
        c.setopt(c.VERBOSE, True)
        c.setopt(pycurl.CUSTOMREQUEST,"POST")
        c.setopt(pycurl.POSTFIELDS,s)
        c.setopt(c.WRITEFUNCTION,buf.write)

        c.perform()
        c.close()


        print buf.getvalue()
        buf.close()
    except pycurl.error, error:
        errno, errstr = error
        print 'An error occurred: ', errstr

getPostvalue()

'''
post_data_dic={"name":"value"}
crl=pycurl.Curl()
crl.setopt(pycurl.VERBOSE,1)
crl.setopt(pycurl.FOLLOWLOCATION,1)
crl.setopt(pycurl.MAXREDIRS,5)

crl.setopt(pycurl.CONNECTTIMEOUT,60)
crl.setopt(pycurl.TIMEOUT,300)

crl.setopt(pycurl.HTTPPROXYTUNNEL,1)

crl.fp= cStringIO.StringIO()
crl.setopt(pycurl.USERAGENT,"dhguhoho")

crl.setopt(crl.POSTFIELDS,urllib.urlencode(post_data_dic))
crl.setopt(pycurl.URL,'http://127.0.0.1:8080')
crl.setopt(crl.WRITEFUNCTION,crl.fp.write)
crl.perform()
print crl.fp.getvalue()
'''