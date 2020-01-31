from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views import View
from ..utils import isUserLoggedIn, gernerateUserToken
from wrw.models import Symptom, User


class IndexPage(View):
    template_name = 'pages/index.html'

    def post(self, request, *args, **kwargs):
        params = request.POST

        username = params['username'] if 'username' in params else None
        password = params['password'] if 'password' in params else None

        try:
            user = User.objects.get(username=username, password=password)
            token = gernerateUserToken(user)

            request.session['wrw_token'] = token
        except ObjectDoesNotExist:
            kwargs['incorrect_login'] = True
            pass

        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if 'action' in request.GET and request.GET['action'] == 'logout':
            request.session.flush()
            return HttpResponseRedirect('/')

        userId = isUserLoggedIn(request)

        if userId:
            return HttpResponseRedirect('/user/%s' % userId)

        incorrect_login = True if 'incorrect_login' in kwargs else False

        return render(request, self.template_name, dict(
            symptoms=Symptom.objects.all(),
            incorrect_login=incorrect_login
        ))
