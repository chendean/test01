__author__ = 'leon'

import urllib

'''
url = 'http://127.0.0.1:8080/'


params = urllib.urlencode({
    'name': 'fadfa'
})

data = urllib.urlopen(url, params).read()
print data
'''
url = 'http://127.0.0.1:8080/'
u = urllib.urlopen(url)
# u is a file-like object
data = u.read()
print data




