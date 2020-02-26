from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views import View
from ..utils import isUserLoggedIn
from wrw.models import Symptom, User


class SymptomPage(View):
    template_name = 'pages/symptom.html'

    def get(self, request, *args, **kwargs):
        user_id = isUserLoggedIn(request)

        if not user_id:
            return HttpResponseRedirect('/')

        try:
            user = User.objects.get(id=user_id)
        except:
            return HttpResponse('No user.')

        symptom_id = kwargs['symptom_id'] if 'symptom_id' in kwargs else None

        if symptom_id is None:
            return HttpResponse('Provided Parameter is invalid.')

        symptom = Symptom.objects.get(id=symptom_id)

        rows = []

        return render(request, self.template_name, dict(symptom=symptom, rows=rows))
