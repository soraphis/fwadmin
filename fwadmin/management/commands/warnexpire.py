import datetime
import os

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from django_project.settings import (
    WARN_EXPIRE_EMAIL_FROM,
    WARN_EXPIRE_DAYS,
    WARN_EXPIRE_URL_TEMPLATE,
)
from fwadmin.models import Host

# run command as:
#   python manage.py warnexpire 14

def send_renew_mail(host):
    url = WARN_EXPIRE_URL_TEMPLATE % {
        'url': reverse("fwadmin:edit_host", args=(host.pk,)),
        }
    # the text
    subject = _("Firewall config for '%s'") % host.name
    body = _("""Dear %(user)s,

The firewall config for machine: '%(host)s' (%(ip)s) will expire at
'%(expire_date)s'.

Please click on %(url)s to renew.
""") % { 'user': host.owner.username,
        'host': host.name,
         'ip': host.ip,
         'expire_date': host.active_until,
         'url': url,
       }
    if "FWADMIN_DRY_RUN" in os.environ:
        print "From:", WARN_EXPIRE_EMAIL_FROM
        print "To:", host.owner.email
        print "Subject: ", subject
        print body
        print 
    else:
        send_mail(subject, body, WARN_EXPIRE_EMAIL_FROM, [host.owner.email])


class Command(BaseCommand):
    help = 'send warning mails when expire is close, first arg is nr of days'

    def handle(self, *args, **options):
        days_delta = WARN_EXPIRE_DAYS
        td = datetime.timedelta(days=days_delta)
        for host in Host.objects.all():
            if (host.active_until-td < datetime.date.today() and
                host.approved and
                host.active):
                send_renew_mail(host)

