#!/bin/bash

cd /opt/sk8ts

# All the playbooks to run
playbooks="aws-infrastructure.yml
certificate-authority.yml
etcd-cluster.yml
k8s-controller.yml
k8s-public-api.yml
k8s-workers.yml
kubectl-client.yml
"

ansible="/opt/sk8ts-venv/bin/ansible"


for p in ${playbooks}; do
  if ! ansible-playbooke ${p}; then
    echo "ERROR: ${p} failed, exiting..."
    exit 1
  fi
done
  
