import datetime

from django.core.management.base import BaseCommand

from fwadmin.models import Host

# run command as:
#   python manage.py warnexpire 14

def send_renew_mail(host):
    # XXX: HARDCODED OOOHHHH NO
    url="http://fwadmin.uni-trier.de/"
    # the text
    text = """Machine: '%(host)s' (%(ip)s
Your firewall configuration will expire at '%(expire_date)s'. 

Please click on %(url)s to renew.
""" % {'host': host.name,
       'ip': host.ip,
       'expire_date': host.active_until,
       'url': url,
       }
    print text
    print host.owner.username, host.owner.email


class Command(BaseCommand):
    help = 'send warning mails when expire is close, first arg is nr of days'

    def handle(self, *args, **options):
        days_delta = int(args[0])
        td = datetime.timedelta(days=days_delta)
        for host in Host.objects.all():
            if (host.active_until-td < datetime.date.today() and
                host.approved and
                host.active):
                send_renew_mail(host)

