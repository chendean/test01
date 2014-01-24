#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
__version__ = "0.0"
__author__ = 'Mkk'

import web
from web.contrib.template import render_mako
from BigoCfgWeb import urls
from BigoCommon import sql
from BigoCommon import base
import json

render = render_mako(
    directories=['templates'],
    input_encoding='utf-8',
    output_encoding='utf-8',
)

class tbselect(base.WebBase):
    def get(self):
        if(self.Valid()):
            #Read Selected Tables
            vtables = []
            vviews = []
            if "tabledic" in urls.session.dbs:
                for val in urls.session.dbs["tabledic"]:
                    if "objname" in val:
                        if "type" in val and val["type"] == "v":
                            vviews.append({"text":val["objname"]});
                        else:
                            vtables.append({"text":val["objname"]});

            tablesstr = vtables.__str__().replace("u'","'").replace("'", '"')
            viewsstr = vviews.__str__().replace("u'","'").replace("'", '"')
            return  render.dbs_tbselect(tables=tablesstr,views = viewsstr)
        else:
            return "<script type='text/javascript'>window.location.href = '\dbs_cnncfg'</script>"
    def post(self):
        if(self.Valid()):
            i=web.input()
            tables = []
            for name in i:
                if "views" in name:tp = "v"
                else:tp = "t"
                tables.append({'objname':i[name], 'type':tp, 'incremental':'', 'filters':'', 'col':'', 'pk':'','sql':'', 'condition': '',  'ng': ''})
            urls.session.dbs["tabledic"] = tables
            print tables
            return  True
        else:
            return False
    def Valid(self):
        if("dbs" in urls.session and "db" in urls.session["dbs"]):
            return True
        else:
            return False

class gettable(base.WebBase):
    def get(self):
        i = web.input();
        from BigoCommon import db
        cnn = urls.session.dbs["db"]
        userdb = db.database(dbn = cnn['dbn'], db = cnn['db'], user = cnn['user'],pw = cnn['pw'],host=cnn['host'])
        tablequery = sql.sqlquery(cnn['dbn'],userdb)
        if 'type' in i and i['type'] == 'v':
            tables = tablequery.showviews()
        else:
            tables = tablequery.showtables()

        str = tables.__str__().replace("'",'"');
        #返回结果中含有unicode的场合转str会带来多余的符号导致控件无法识别
        if '": u"' in str:
            str=str.replace('": u"', '": "')

        return str;