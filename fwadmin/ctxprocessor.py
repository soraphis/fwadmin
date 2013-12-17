from .auth import is_moderator


def user_auth(request):
    return {'user_is_moderator': is_moderator(request.user),
           }
