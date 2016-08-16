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
import warnings


class CloudFormsInventory(object):

    def _empty_inventory(self):
        return {"_meta": {"hostvars": {}}}

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
            data2 = {}
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

        # SSL Verification
        if config.has_option('cloudforms', 'ssl_verify'):
            self.cloudforms_ssl_verify = config.getboolean('cloudforms', 'ssl_verify')
        else:
            self.cloudforms_ssl_verify = False

    def get_hosts(self):
        ''' Gets host from CloudForms '''

        r = requests.get("https://{0}/api/vms?expand=resources,tags&attributes=name,power_state,ipaddresses,host_id,"
                         "vendor,cloud,connection_state,location,raw_power_state,created_on,id,template,type".format(
                             self.cloudforms_hostname), auth=(self.cloudforms_username, self.cloudforms_password),
                         verify=self.cloudforms_ssl_verify)
        try:
            obj = r.json()
        except ValueError:
            warnings.warn("Unexpected response from {0} ({1}): {2}".format(self.cloudforms_hostname, r.status_code,
                                                                           r.reason))
            obj = {}

        # Create groups+hosts based on host data
        for resource in obj.get('resources', []):
            # Ignore VMS that are not powered on
            if resource['power_state'] != "on":
                continue

            # Create a 'cloudforms' group
            if 'cloudforms' not in self.inventory:
                self.inventory['cloudforms'] = []

            # Add host to 'cloudforms' group
            self.inventory['cloudforms'].append(resource['name'])

            # Create additional groups
            for key in ('vendor', 'type', 'location'):
                if key in resource:

                    # Create top-level group
                    if key not in self.inventory:
                        self.inventory[key] = dict(children=[], vars={}, hosts=[])

                    # Create sub-group
                    if resource[key] not in self.inventory:
                        self.inventory[resource[key]] = dict(children=[], vars={}, hosts=[])

                    # Add sub-group, as a child of top-level
                    if resource[key] not in self.inventory[key]['children']:
                        self.inventory[key]['children'].append(resource[key])

                    # Add host to sub-group
                    if resource['name'] not in self.inventory[resource[key]]:
                        self.inventory[resource[key]]['hosts'].append(resource['name'])

            # Set ansible_ssh_host to the first available ip address
            if 'ipaddresses' in resource and resource['ipaddresses'] and isinstance(resource['ipaddresses'], list):
                resource['ansible_ssh_host'] = resource['ipaddresses'][0]

            # Add _meta hostvars
            self.inventory['_meta']['hostvars'][resource['name']] = resource

        print json.dumps(self.inventory, indent=2)

# Run the script
CloudFormsInventory()
