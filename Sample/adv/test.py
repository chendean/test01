__author__ = 'leon'

import Sample.test10


def f(a, b, c):
    print a, b, c

f(1, 2, 3)

f(c=3, b=2, a=1)

f(1, c=3, b=2)

def f(a, b, c=10):
    print a, b, c

f(3, 2)
f(3, 2, 1)

def func(*name):
    print type(name)
    print name

func(1, 4, 6)
func(5, 6, 7, 1, 2, 3)