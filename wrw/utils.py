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


def calcScore(severities=[]):
    start_severity = severities[0] - 1
    end_severity = severities[-1] - 1

    actual = end_severity - start_severity
    max_pos = 4 - start_severity
    max_neg = 0 - start_severity

    try:
        score = (-100 * actual /
             max_pos) if actual > 0 else (100 * actual/max_neg)
    except:
        score = 0

    return score
