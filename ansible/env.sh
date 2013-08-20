#!/bin/bash

BASEDIR="$(dirname $(pwd)/$(basename $0))"

ANSIBLE_HOSTS="${BASEDIR}/inventory/ansible_hosts"
export ANSIBLE_HOSTS

echo "Using ansible hosts $ANSIBLE_HOSTS"

mkdir -p "$BASEDIR/non-git-files"
LDAP_PW_FILE="$BASEDIR/non-git-files/ldap-password"
if [ ! -e "$LDAP_PW_FILE" ]; then
    # read -s is a bashism
    read -s -p 'Please enter the ldap password: ' LDAP_PW
    echo -n "$LDAP_PW" > $LDAP_PW_FILE
    echo ""
fi

DB_PW_FILE="$BASEDIR/non-git-files/db-password"
if [ ! -e "$DB_PW_FILE" ]; then
    # read -s is a bashism
    read -s -p 'Please enter the db password: ' DB_PW
    echo -n "$DB_PW" > $DB_PW_FILE
    echo ""
fi
