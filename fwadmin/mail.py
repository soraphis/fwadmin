from django.core.mail import send_mail as django_send_mail
from django.conf import settings


def send_mail(*args, **kwargs):
    if not settings.FWADMIN_REALLY_SEND_MAIL:
        print "About to send mail", args, kwargs
        return
    return django_send_mail(*args, **kwargs)
