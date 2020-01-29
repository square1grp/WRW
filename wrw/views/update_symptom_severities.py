from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from wrw.models import User, Symptom, CurrentUserSymptom, UserSymptomSeverities, UserSingleSymptomSeverity
from wrw.utils import isUserLoggedIn
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt


class UpdateSymptomSeveritiesPage(View):
    template_name = 'pages/update-symptom-severities.html'

    def updateCUSs(self, user, symptomIDs=[]):
        symptoms = Symptom.objects.filter(id__in=symptomIDs)

        cus_list = CurrentUserSymptom.objects.filter(
            user=user).exclude(symptom__id__in=symptomIDs)
        for cus in cus_list:
            cus.delete()

        for symptom in symptoms:
            try:
                CurrentUserSymptom.objects.get(user=user, symptom=symptom)
            except ObjectDoesNotExist:
                cus = CurrentUserSymptom(user=user, symptom=symptom)
                cus.save()

    def createUpdateSymptomSeverities(self, user, date, time, title):
        created_at = datetime.strptime(
            '%s %s' % (date, time), '%m/%d/%Y %H:%M:%S')

        uss = UserSymptomSeverities(
            user=user, title=title, created_at=created_at)
        uss.save()

        return uss

    def createUserSingleSymptomSeverity(self, uss, symptom, selected_level, description):
        usss = UserSingleSymptomSeverity(symptom=symptom, user_symptom_severities=uss,
                                         selected_level=selected_level, description=description)

        usss.save()

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

        # update Current User Symptoms
        self.updateCUSs(user, params.getlist('symptom_IDs'))

        # create Update Symptom Severities
        uss = self.createUpdateSymptomSeverities(
            user, params['date'], params['time'], params['title'])

        for symptom_id in params.getlist('symptom_IDs'):
            symptom = Symptom.objects.get(id=symptom_id)

            description_key = 'symptom_%s_description' % symptom_id

            description = params[description_key] if description_key in params else ''

            try:
                selected_level = params['symptom_%s_level' % symptom_id]

                self.createUserSingleSymptomSeverity(
                    uss, symptom, selected_level, description)
            except:
                print('Symptom Level is not selected.')

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
