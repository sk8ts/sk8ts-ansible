#!/usr/bin/env python

import json
import sys
import os

try:
  from boto import ec2
  from boto import utils
except:
  sys.stderr.write("ERROR: Can't import boto, please install it\n")
  sys.exit(1)

#
# Initialize inventory
# 

inventory = {}
inventory['_meta'] = { 'hostvars': {} }
inventory['all'] = []
# Want everything but localhost used in sk8ts-ansible
inventory['all_instances'] = []

try:
  instance_identity = utils.get_instance_identity()
  aws_region = instance_identity['document']['region']
except:
  sys.stderr.write('ERROR: Could not get region name from instance metadata\n')
  sys.exit(1)
  
#
# Make boto connection
#

# Make the connection to AWS API
try:
  ec2conn = ec2.connect_to_region(aws_region)
except:
  print "ERROR: Unable to connect to AWS"
  sys.exit(1)

for i in  ec2conn.get_only_instances():

  # Check if the host has a name, if not we don't care about it anyways
  try:
    host_name = i.tags['Name']
  except:
    host_name = False

  if i.state == "running" and host_name:

    # Check for a public IP, if non use the private IP
    if i.ip_address:
      ip =  i.ip_address
    else:
      ip =  i.private_ip_address

    # kubernetes role...
    try:
      krole = "tag_krole_" + i.tags['krole']
    except: 
      krole = None

    if krole != None:
      try:
        inventory[krole].append(host_name)
      except:
        inventory[krole] = []    
        inventory[krole].append(host_name)

      # Only want hosts with a krole, ignore all others
      inventory['all'].append(host_name)
      inventory['all_instances'].append(host_name)
      inventory['_meta']['hostvars'][host_name] = {}
      inventory['_meta']['hostvars'][host_name]['ansible_ssh_host'] = ip

print(json.dumps(inventory, indent=4))
