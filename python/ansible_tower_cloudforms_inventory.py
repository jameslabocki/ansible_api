#!/usr/bin/python

'''
CloudForms external inventory script
==================================================
Generates inventory that Ansible can understand by making API request to CloudForms.
Modeled after https://raw.githubusercontent.com/ansible/ansible/stable-1.9/plugins/inventory/ec2.py
jlabocki <at> redhat.com or @jameslabocki on twitter
'''

import os
import argparse
import ConfigParser
import requests
import json


class CloudFormsInventory(object):

    def _empty_inventory(self):
        return {"_meta" : {"hostvars" : {}}}

    def __init__(self):
        ''' Main execution path '''

        # Inventory grouped by instance IDs, tags, security groups, regions,
        # and availability zones
        self.inventory = self._empty_inventory()

        # Index of hostname (address) to instance ID
        self.index = {}

        # Read CLI arguments
        self.read_settings()
        self.parse_cli_args()

        # Get Hosts
        if self.args.list:
            self.get_hosts()

        # This doesn't exist yet and needs to be added
        if self.args.host:
            data2 = { }
            print json.dumps(data2, indent=2)

    def parse_cli_args(self):
        ''' Command line argument processing '''

        parser = argparse.ArgumentParser(description='Produce an Ansible Inventory file based on CloudForms')
        parser.add_argument('--list', action='store_true', default=False,
                           help='List instances (default: False)')
        parser.add_argument('--host', action='store',
                           help='Get all the variables about a specific instance')
        self.args = parser.parse_args()

    def read_settings(self):
        ''' Reads the settings from the cloudforms.ini file '''

        config = ConfigParser.SafeConfigParser()
        config_paths = [
            os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cloudforms.ini'),
            "/etc/ansible/cloudforms.ini",
        ]

        env_value = os.environ.get('CLOUDFORMS_INI_PATH')
        if env_value is not None:
            config_paths.append(os.path.expanduser(os.path.expandvars(env_value)))

        config.read(config_paths)

        # Version
        if config.has_option('cloudforms', 'version'):
            self.cloudforms_version = config.get('cloudforms', 'version')
        else:
            self.cloudforms_version = "none"

        # CloudForms Endpoint
        if config.has_option('cloudforms', 'hostname'):
            self.cloudforms_hostname = config.get('cloudforms', 'hostname')
        else:
            self.cloudforms_hostname = None

        # CloudForms Username
        if config.has_option('cloudforms', 'username'):
            self.cloudforms_username = config.get('cloudforms', 'username')
        else:
            self.cloudforms_username = "none"

        # CloudForms Password
        if config.has_option('cloudforms', 'password'):
            self.cloudforms_password = config.get('cloudforms', 'password')
        else:
            self.cloudforms_password = "none"

        # CloudForms Password
        if config.has_option('cloudforms', 'ssl_verify'):
            self.cloudforms_ssl_verify = config.getboolean('cloudforms', 'ssl_verify')
        else:
            self.cloudforms_ssl_verify = False

    def get_hosts(self):
        ''' Gets host from CloudForms '''
        r = requests.get("https://" + self.cloudforms_hostname + "/api/vms?expand=resources,tags&attributes=name,power_state,ipaddresses,host_id,vendor,cloud,connection_state,raw_power_state,created_on,id,template,type", auth=(self.cloudforms_username,self.cloudforms_password), verify=self.cloudforms_ssl_verify)

        vms = json.loads(r.text)

        hosts = { 'cloudforms': {} }
        hosts['cloudforms']['hosts'] = []
        hosts['_meta'] = { 'hostvars': {}}

        for vm in vms['resources']:
            if vm['power_state'] == "on":
                # we are going to use the name of the vm or the FIRST ip address
                vm_id = vm['name']
                if vm.has_key('ipaddresses') and vm['ipaddresses'][0]:
                    vm_id = vm['ipaddresses'][0]

                if vm.has_key('tags'):
                    for tag in vm['tags']:
                        if hosts.has_key(tag['name']):
                            hosts[tag['name']].append(vm_id)
                        else:
                            hosts[tag['name']] = [vm_id]

                hosts['cloudforms']['hosts'].append(vm_id)

                hosts['_meta']['hostvars'][vm_id] = {
                    'cloud': vm['cloud'],
                    'connection_state': vm['connection_state'],
                    'created_on': vm['created_on'],
                    'host_id': vm['host_id'],
                    'id': vm['id'],
                    'name': vm['name'],
                    'power_state': vm['power_state'],
                    'raw_power_state': vm['raw_power_state'],
                    'template': vm['template'],
                    'type': vm['type'],
                    'vendor': vm['vendor'],
                }

        print json.dumps(hosts, sort_keys=True, indent=2)

# Run the script
CloudFormsInventory()

