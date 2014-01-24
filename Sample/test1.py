__author__ = 'leon'

'''
f = open('1.txt')

f.next()
f.next()
f.next()
for line in open('1.txt'):
    print line


G = (x for x in range(4))
for i in G:
    print i


xl = [1,3,5]
yl = [9,12,13]
L = [ x**2 for (x,y) in zip(xl,yl) if y > 10]

print L
'''

def func(a):
    if a > 100:
        return True
    else:
        return False

print filter(func, [10, 56, 101, 500])

print reduce((lambda x, y: x + y), [1, 2, 5, 7, 9])

re = iter(range(5))

try:
    for i in range(100):
        print re.next()
except StopIteration:
    print 'here is end ', i

print 'HaHaHaHa'

print 'Lalala'
raise StopIteration
print 'Hahaha'