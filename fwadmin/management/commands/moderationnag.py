from django.utils.translation import ugettext as _
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse

from django_project.settings import (
    FWADMIN_MODERATION_WAITING_MAIL_NAG,
    WARN_EXPIRE_EMAIL_FROM,
    WARN_EXPIRE_URL_TEMPLATE,
)

from fwadmin.models import (
    Host,
)


def send_moderation_nag_mail():
    path = reverse("fwadmin:moderator_list_unapproved")
    url = WARN_EXPIRE_URL_TEMPLATE % {'url': path}
    subject = _("fwadmin hosts waiting for moderation")
    hosts_from_db = Host.objects.filter(approved=False)
    if hosts_from_db:
        hosts = ["%s (%s)" % (host.name, host.ip) for host in hosts_from_db]
        body = _("""The hosts below need moderation. You can approve via:
%(url)s

Hosts waiting for moderation:
%(hosts)s""") % {'hosts': "\n".join(hosts),
                 'url': url,
                 }
        send_mail(subject, body, WARN_EXPIRE_EMAIL_FROM,
                  [FWADMIN_MODERATION_WAITING_MAIL_NAG])


class Command(BaseCommand):
    help = 'send nag mail about hosts waiting for approval'

    def handle(self, *args, **options):
        send_moderation_nag_mail()
