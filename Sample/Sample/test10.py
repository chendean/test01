__author__ = 'leon'
#coding:utf-8
print dir(list)

#print help(str)

print [1, 2, 3] + [5, 6, 9]

class superList(list):
    def __sub__(self, b):
        a = self[:]     # 这里，self是supeList的对象。由于superList继承于list，它可以利用和list[:]相同的引用方法来表示整个对象。
        b = b[:]
        while len(b) > 0:
            element_b = b.pop()
            if element_b in a:
                a.remove(element_b)
        return a

print superList([1, 2, 3]) - superList([3, 4])