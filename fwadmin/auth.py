from django.core.exceptions import PermissionDenied
from django.http import (
    HttpResponseForbidden,
)
from django.contrib.auth.decorators import (
    user_passes_test,
)
from django.conf import settings


# auth releated stuff
def group_required(group_name):
    """ Custom decorator that will raise a PermissionDendied if not in the
        right group
    """
    def is_in_group(user, group_name):
        if user:
            if user.groups.filter(name=group_name).count() == 1:
                return True
        # XXX: add template with logout form here
        raise PermissionDenied("You are not in group '%s'" % group_name)
    return user_passes_test(lambda u: is_in_group(u, group_name))


class NotOwnerError(HttpResponseForbidden):
    """A error if the user is not the owner of the object he/she tries
       to modify
    """
    def __init__(self, user):
        super(HttpResponseForbidden, self).__init__(
            "You (%s) are not owner of this object" % user.username)


def is_moderator(user):
    return user.groups.filter(
        name=settings.FWADMIN_MODERATORS_USER_GROUP).count() > 0


def user_has_permssion_for_host(host, user):
    return host.owner == user or is_moderator(user)
