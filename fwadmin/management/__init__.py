from django.db.models.signals import post_syncdb

from django.contrib.auth.models import (
    Group,
)

from django.conf import settings


# XXX: should we map to permissions instead?
def add_fwuser_group(sender, **kwargs):
    # make sure the group for firewall user exists in the database
    (group, created) = Group.objects.get_or_create(
        name=settings.FWADMIN_ALLOWED_USER_GROUP)
    # and for the moderators as well
    (group, created) = Group.objects.get_or_create(
        name=settings.FWADMIN_MODERATORS_USER_GROUP)


post_syncdb.connect(add_fwuser_group)
