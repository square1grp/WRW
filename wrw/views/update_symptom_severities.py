from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from wrw.models import User, Symptom, CurrentUserSymptom
from wrw.utils import isUserLoggedIn
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt


class UpdateSymptomSeveritiesPage(View):
    template_name = 'pages/update-symptom-severities.html'

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        user_id = isUserLoggedIn(request)

        if not user_id:
            return HttpResponseRedirect('/')

        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return HttpResponse('No user.')

        params = request.POST

        import pdb; pdb.set_trace()

        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user_id = isUserLoggedIn(request)

        if not user_id:
            return HttpResponseRedirect('/')

        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return HttpResponse('No user.')

        cus_list = CurrentUserSymptom.objects.filter(user=user)

        symptoms = []

        for symptom in Symptom.objects.all():
            _symptom = dict(id=symptom.id, name=symptom.name, disabled=False)
            try:
                CurrentUserSymptom.objects.get(user=user, symptom=symptom)

                _symptom['disabled'] = True
            except ObjectDoesNotExist:
                pass

            symptoms.append(_symptom)

        org_symptoms = [dict(
            id=symptom.id,
            name=symptom.name,
            levels=symptom.getSymptomLevels()
        ) for symptom in Symptom.objects.all()]

        return render(request, self.template_name, dict(
            user_id=user_id,
            cus_list=cus_list,
            symptoms=symptoms,
            org_symptoms=org_symptoms,
            current_time=dict(h='%02d' % datetime.now().hour,
                              m='%02d' % datetime.now().minute,
                              s='%02d' % datetime.now().second)
        ))
