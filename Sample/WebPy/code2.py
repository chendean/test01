__author__ = 'leon'
#coding:utf-8

import web
import json
import pymssql

render = web.template.render('templates')
db = web.database(dbn = 'mssql', db = 'DKI', user = 'sa', pw = '!QAZ2wsxb1g0',host='192.168.0.32',port =1433,charset="utf8")
urls = (
    '/', 'index'
    )



class index:
    def GET(self):
        trans = db.transaction()
        out = db.query("select CustomerID, MamaName, StatusID, DueDate, BabyName from dbo.Customer_test")
        #print(out.list())
        trans.commit()

        '''
        con=pymssql.connect(host='192.168.0.32',user='sa',password='!QAZ2wsxb1g0',database= 'DKI',charset="utf8")
        cur=con.cursor()
        cur.execute('select * from Customer_test')
        print cur.fetchall()
        cur.close()
        con.close()
        '''
        aaa=out.list()
        print aaa
        for i in aaa:
            print i.MamaName
        aa=''
        return render.sample2(aa)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

