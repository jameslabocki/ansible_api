#!/usr/bin/python

import requests
import pprint

r = requests.get("http://YOURTOWERIP/api/v1/hosts", auth=('admin', 'YOURPASSWORD'))

pp = pprint.PrettyPrinter(indent=4)

pp.pprint(r.json())
