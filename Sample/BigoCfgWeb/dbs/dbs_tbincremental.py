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


class tbincremental(base.WebBase):
    def get(self):
        if(self.Valid()):
            #Read Selected Tables
            vtables = []
            vviews = []
            if "tabledic" in urls.session.dbs:
                for val in urls.session.dbs["tabledic"]:
                    if "objname" in val and "incremental" in val and val["incremental"] == "true":
                        if "type" in val and val["type"] == "v":
                            vviews.append({"text":val["objname"]});
                        else:
                            vtables.append({"text":val["objname"]});

            tablesstr = vtables.__str__().replace("u'","'").replace("'", '"')
            viewsstr = vviews.__str__().replace("u'","'").replace("'", '"')
            return  render.dbs_tbincremental(tables=tablesstr,views = viewsstr)
        else:
            return "<script type='text/javascript'>window.location.href = '\dbs_cnncfg'</script>"
    def post(self):
        if(self.Valid()):
            iput=web.input()
            tables = urls.session.dbs["tabledic"]
            for tb in tables:
                tb["incremental"] = "false"
            for i in iput:
                for tb in tables:
                    if iput[i] == tb["objname"]:
                        tb["incremental"] = "true"

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
        vtables = []
        vviews = []
        if "tabledic" in urls.session.dbs:
            for val in urls.session.dbs["tabledic"]:
                if "objname" in val and "incremental" in val:
                    if "type" in val and val["type"] == "v":
                        vviews.append({"text":val["objname"]});
                    else:
                        vtables.append({"text":val["objname"]});

        if 'type' in i and i['type'] == 'v':
            vtables = vviews

        str = vtables.__str__().replace("u'","'").replace("'", '"')
        return str;