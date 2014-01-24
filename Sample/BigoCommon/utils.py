# -*- coding: utf-8 -*-
__author__ = 'Dean'

__all__ = [
    "dicsort", "diclistsort",
    "diclistSortasDate",
    ]
#字典排序，
#dic: 字典
#sort: 'asc' or 'desc'
#sortkey: True(按key排序)  False(按value排序)
def dicsort(dic, sortfield, sort='asc' ):
    import operator
    if (sort=='asc'):
        dic.sort(key=operator.itemgetter(sortfield))
    else:
        dic.sort(key=operator.itemgetter(sortfield),reverse=True)
    return dic


#字典list的排序
#list: 字典list
#sort: 'asc' or 'desc'
#sortfield: 字典中的排序项

def diclistsort(list,sortfield,sort='asc'):
    if (sort=='asc'):
        return sorted(list,cmp=lambda x,y:cmp(x[sortfield],y[sortfield]),reverse=False)
    else:
        return sorted(list,cmp=lambda x,y:cmp(x[sortfield],y[sortfield]),reverse=True)


#字典list的排序(时间格式)
#list: 字典list
#sort: 'asc' or 'desc'
#sortfield: 字典中的排序项
def diclistSortasDate(list,sortfield,sort='asc'):
    import operator
    try:
        if (sort=='asc'):
            list.sort(cmp=cmp_datetime, key=operator.itemgetter('createdate'))
        else:
            list.sort(cmp=cmp_datetime, key=operator.itemgetter('createdate'),reverse=True)
    except Exception,ex:
        print ex
    finally:
        return list

def cmp_datetime(a, b, format='%Y-%m-%d %H:%M:%S'):
    import datetime
    try:
        a_datetime = datetime.datetime.strptime(a, format)
        b_datetime = datetime.datetime.strptime(b, format)

        if a_datetime > b_datetime:
            return -1
        elif a_datetime < b_datetime:
            return 1
        else:
            return 0
    except Exception,ex:
        print ex
        return -1

