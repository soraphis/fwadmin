#!/bin/sh

BASEDIR="$(dirname $(pwd)/$(basename $0))"

ANSIBLE_HOSTS="${BASEDIR}/inventory/ansible_hosts"
export ANSIBLE_HOSTS

echo "Using ansible hosts $ANSIBLE_HOSTS"
