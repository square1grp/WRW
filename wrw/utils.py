import base64
from wrw.models import User
from django.core.exceptions import ObjectDoesNotExist


def isUserLoggedIn(request):
    token = request.session.get('wrw_token', False)

    if token:
        try:
            [username, password] = base64.b64decode(
                token).decode().split(' ||| ')

            user = User.objects.get(username=username, password=password)

            return user.id
        except ObjectDoesNotExist:
            pass

    return False


def gernerateUserToken(user):
    return base64.b64encode(
        ('%s ||| %s' % (user.username, user.password)).encode()).decode()
