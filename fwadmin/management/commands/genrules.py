import datetime
import logging

from django.core.management.base import BaseCommand

from fwadmin.models import Host


class BaseRulesWriter:
    """Base class for writing host rules"""

    def get_rules_list(self, host):
        """Return a list of strings with rules for this specific host"""
        raise Exception("NotImplemented")


class CiscoRulesWriter(BaseRulesWriter):

    def get_rules_list(self, host):
        l = []
        l.append("! fw rules for %s (%s) owner by %s" % (
                host.name, host.ip, host.owner))
        # XXX: how to get the access-list number?
        list_nr = 120
        # XXX: add allow_from to Port
        from_location = "any" #port.allow_from
        for port in host.open_ports.all():
            s = ("access-list %(list_nr)s "
                 "permit %(type)s %(from)s host %(ip)s eq %(port)s" % {
                    'list_nr': list_nr,
                    'type': port.type,
                    'from': from_location,
                    'ip': host.ip,
                    'port': port.number})
            l.append(s)
        return l


class Command(BaseCommand):
    help = 'write the firewall rules to stdout'

    def handle(self, *args, **options):
        writer = CiscoRulesWriter()
        for host in Host.objects.all():
            if (host.active_until > datetime.date.today() and
                host.approved and
                host.active):
                print "\n".join(writer.get_rules_list(host))

