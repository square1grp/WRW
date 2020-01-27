from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views import View
from wrw.models import User


class VerifyTokenPage(View):
    template_name = 'pages/verify.html'

    def get(self, request, *args, **kwargs):
        if 'token' in kwargs:
            confirm_token = kwargs['token']

            if confirm_token and confirm_token[-1] == '/':
                confirm_token = confirm_token[:-1]

            try:
                user = User.objects.get(confirm_token=confirm_token)

                if user.email_to_confirm:
                    user.email = user.email_to_confirm
                    user.email_to_confirm = None

                user.is_approved = True
                user.save()

                return HttpResponseRedirect('/')
            except ObjectDoesNotExist:
                return HttpResponse("check your email")

        return render(request, self.template_name)
