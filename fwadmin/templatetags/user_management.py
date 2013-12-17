from django import template
from django.conf import settings

register = template.Library()


# there must be a better way for global moderator checking
@register.assignment_tag(takes_context=True)
def do_moderator_check(context):
    return context['user'].groups.filter(
        name=settings.FWADMIN_MODERATORS_USER_GROUP).count() > 0
