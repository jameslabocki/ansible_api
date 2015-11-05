#!/usr/bin/python

import requests
import pprint

r = requests.get("http://10.19.1.107/api/v1/hosts", auth=('admin', 'redhat'))

pp = pprint.PrettyPrinter(indent=4)

pp.pprint(r.json())
