#!/usr/bin/python

import urllib2

url = 'http://10.19.1.107/api/v1/'
response = urllib2.urlopen(url).read()

print response
