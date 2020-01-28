from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from wrw.models import User
from wrw.utils import isUserLoggedIn


class UserPage(View):
    template_name = 'pages/user.html'

    def get(self, request, *args, **kwargs):
        user_id = isUserLoggedIn(request)

        if not user_id:
            return HttpResponseRedirect('/')

        try:
            user = User.objects.get(id=user_id)
        except:
            return HttpResponse('No user.')

        return render(request, self.template_name, dict(
            user=user,
        ))
