import requests
import re

import time

url = 'http://dumps.wikimedia.org/other/pagecounts-raw/2013/2013-01/'
data = requests.get(url).text
#print data

# <li><a href="pagecounts-20130101-000000.gz">pagecounts-20130101-000000.gz</a>, size 77M</li>
p = re.compile('pagecounts-\d{4}\d{2}\d{2}-\d{6}.gz')


m=p.findall(data)

#print m

for i in range(len(m)):
    if (i%2==0):
        print m[i]

print len(m)

for i in range(len(m)):
    if (i%2==0):
        print "downloading ",  m[i]
        r = requests.get(url+m[i])
        with open(m[i], "wb") as code:
            code.write(r.content)
        del r