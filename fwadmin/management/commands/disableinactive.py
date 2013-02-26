import logging

from django.core.management.base import BaseCommand

from django_project.settings import (
    AUTH_LDAP_SERVER_URI,
    AUTH_LDAP_USER_SEARCH,
    AUTH_LDAP_BIND_DN,
    AUTH_LDAP_BIND_PASSWORD,
)
from fwadmin.models import Host

# run command as:
#   python manage.py disableinactive

import ldap


def ldap_user_exists(userid):
    ldap.set_option(ldap.OPT_REFERRALS, 0)
    ad = ldap.initialize(AUTH_LDAP_SERVER_URI)
    ad.simple_bind_s(AUTH_LDAP_BIND_DN, AUTH_LDAP_BIND_PASSWORD)
    # this is a LDAPSearch object from django-ldap-auth
    result = AUTH_LDAP_USER_SEARCH.execute(ad, {'user': userid})
    #print result
    return len(result) > 0


class Command(BaseCommand):
    help = 'disable no longer active users'

    def handle(self, *args, **options):
        for host in Host.objects.all():
            if not host.active or not host.approved:
                continue
            if not ldap_user_exists(host.owner.username):
                logging.warning(
                    "User '%s' no longer exists, disabling '%s'" % (
                        host.owner.username, host.ip))
                host.active = False
                host.save()
