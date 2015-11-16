#!/usr/bin/python

import requests

r = requests.post("http://YOURTOWERIP/api/v1/hosts/", data = {"name":"HOSTIPADDRESS", "inventory":1}, auth=('admin', 'YOURPASSWORDHERE'))

print r.text
