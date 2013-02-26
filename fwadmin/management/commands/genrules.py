import datetime

from django.core.management.base import BaseCommand
from django_project.settings import FWADMIN_ACCESS_LIST_NR

from fwadmin.models import (
    ComplexRule,
    Host,
)


class BaseRulesWriter:
    """Base class for writing host rules"""

    def get_rules_list(self, host):
        """Return a list of strings with rules for this specific host"""
        raise Exception("NotImplemented")


class CiscoRulesWriter(BaseRulesWriter):

    def _get_fw_string(self, list_nr, permit, type, from_net, to_ip, port):
        # HRM, ugly and lacks tests!
        d = {'list_nr': list_nr,
             'type': type,
             'from_net': from_net,
             'to_ip': to_ip,
             'port': "",
            }
        if permit:
            d["permit_or_deny"] = "permit"
        else:
            d["permit_or_deny"] = "deny"
        # port is optional I think
        if port:
            d["port"] = "eq %s" % port
        s = ("access-list %(list_nr)s %(permit_or_deny)s %(type)s "
             "%(from_net)s host %(to_ip)s %(port)s" % d)
        return s

    def get_rules_list(self, host):
        l = []
        l.append("! fw rules for %s (%s) owned by %s" % (
                host.name, host.ip, host.owner))
        list_nr = FWADMIN_ACCESS_LIST_NR
        # complex rules
        for complex_rule in ComplexRule.objects.filter(host=host):
            s = self._get_fw_string(list_nr=list_nr,
                                    permit=complex_rule.permit,
                                    type=complex_rule.ip_protocol,
                                    from_net=complex_rule.from_net,
                                    to_ip=host.ip,
                                    port=complex_rule.port)
            l.append(s)
        return l


class Command(BaseCommand):
    help = 'write the firewall rules to stdout'

    def _write_rules(self, rules_list):
        print "\n".join(rules_list)

    def print_firewall_rules(self):
        writer = CiscoRulesWriter()
        for host in Host.objects.all():
            if (host.active_until > datetime.date.today() and
                host.approved and
                host.active):
                rules_list = writer.get_rules_list(host)
                self._write_rules(rules_list)

    def handle(self, *args, **options):
        self.print_firewall_rules()
