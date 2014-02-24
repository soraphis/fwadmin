from django.contrib import messages
from django.contrib.auth.signals import user_logged_out, user_logged_in
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _


@receiver(user_logged_out)
def on_user_logged_out(sender, request, **kwargs):
    messages.success(request,
        _("You're logged out. Thanks for using the firewall admin."))


@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    messages.success(request,
        _("You're logged in as %s. Welcome!") % user,
        fail_silently=True)
