__author__ = 'leon'

for a in [3, 4.4, 'life']:
    print a

idx = range(5)
print idx

for a in range(10):
    print a ** 2

i = 0
while i < 10:
    print i
    i = i + 1

i = 0
print  range(10)[9]
while i <= range(10)[9]:
    print i
    i = i + 1


for i in range(10):
    if i == 2:
        continue
    print i

for i in range(10):
    if i == 2:
        break
    print i