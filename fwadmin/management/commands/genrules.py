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
        # XXX check if comments are allowed
        l.append("# fw rules for %s (%s) owner by %s" % (
                host.name, host.ip, host.owner))
        for port in host.open_ports.all():
            # XXX: check synatax
            s = "from any to %s allow %s %s" % (
                host.ip, port.type, port.number)
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

