#!/usr/bin/python

import requests

r = requests.post("http://10.19.1.107/api/v1/hosts/", data = {"name":"10.19.1.113", "inventory":1}, auth=('admin', 'redhat'))

print r.text
