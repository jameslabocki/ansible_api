#!/usr/bin/python

import urllib
import urllib2

url = 'http://10.19.1.107/api/v1/hosts/'
params = urllib.urlencode({
  'firstName': 'John',
  'lastName': 'Doe'
})
response = urllib2.urlopen(url, params).read()

