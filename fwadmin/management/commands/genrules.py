import sys

from django.core.management.base import BaseCommand
from fwadmin.genrules import gen_firewall_rules


class Command(BaseCommand):
    help = 'write the firewall rules to stdout'

    OUTPUT = sys.stdout

    def handle(self, *args, **options):
        # default writer is cisco
        if not args:
            fwtype = "cisco"
        else:
            fwtype = args[0]
        gen_firewall_rules(self.OUTPUT, fwtype)
