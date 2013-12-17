from .auth import is_moderator


def user_auth(request):
    return {'is_moderator': is_moderator(request.user),
           }
