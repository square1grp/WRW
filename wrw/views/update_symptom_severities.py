from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from wrw.models import User, Symptom, CurrentUserSymptom, UserSymptomSeverities, UserSingleSymptomSeverity
from wrw.utils import isUserLoggedIn
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist


class UpdateSymptomSeveritiesPage(View):
    template_name = 'pages/update-symptom-severities.html'

    def createUserSymptomSeverities(self, user, date, time, title):
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

    def post(self, request, *args, **kwargs):
        user_id = isUserLoggedIn(request)

        if not user_id:
            return HttpResponseRedirect('/')

        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return HttpResponse('No user.')

        params = request.POST

        if params['action'] == 'add':
            if 'selected_uss_id' in params:
                # update Update Symptom Severities
                uss = UserSymptomSeverities.objects.get(
                    id=params['selected_uss_id'])

                uss.created_at = datetime.strptime(
                    '%s %s' % (params['date'], params['time']), '%m/%d/%Y %H:%M:%S')
                uss.title = params['title']

                uss.save()

                usss_list = UserSingleSymptomSeverity.objects.filter(
                    user_symptom_severities=uss)
                for usss in usss_list:
                    usss.delete()
            else:
                # create User Symptom Severities
                uss = self.createUserSymptomSeverities(
                    user, params['date'], params['time'], params['title'])

            for symptom_id in params.getlist('symptom_IDs'):
                symptom = Symptom.objects.get(id=symptom_id)

                description_key = 'symptom_%s_description' % symptom_id
                description = params[description_key] if description_key in params else ''

                selected_level_key = 'symptom_%s_level' % symptom_id
                selected_level = params[selected_level_key] if selected_level_key in params else None

                self.createUserSingleSymptomSeverity(
                    uss, symptom, selected_level, description)

        elif params['action'] == 'delete':
            uss = UserSymptomSeverities.objects.get(id=params['uss_id'])
            uss.delete()

        elif params['action'] in ['edit', 'date_filter']:
            if 'uss_id' in params:
                kwargs['uss_id'] = params['uss_id']

            if 'date_filter' in params:
                kwargs['date_filter'] = params['date_filter']

        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user_id = isUserLoggedIn(request)

        if not user_id:
            return HttpResponseRedirect('/')

        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return HttpResponse('No user.')

        params = request.GET
        if 'action' in params:
            if params['action'] == 'delete_cus':
                symptom_id = params['symptom_id']
                cus = CurrentUserSymptom.objects.get(
                    user=user, symptom__id=symptom_id)
                cus.delete()

            elif params['action'] == "add_cus":
                symptom_id = params['symptom_id']
                cus = CurrentUserSymptom(
                    user=user, symptom=Symptom.objects.get(id=symptom_id))
                cus.save()

            return HttpResponseRedirect('/user/%s/update_symptom_severities' % user_id)

        cus_list = CurrentUserSymptom.objects.filter(user=user)

        current_date = datetime.now().strftime('%m/%d/%Y')
        current_time = '{}:{}:{}'.format('%02d' % datetime.now().hour,
                                         '%02d' % datetime.now().minute,
                                         '%02d' % datetime.now().second)

        selected_uss = None
        symptoms = []
        if 'uss_id' in kwargs:
            selected_uss = UserSymptomSeverities.objects.get(
                id=kwargs['uss_id'])

            current_date = selected_uss.created_at.strftime('%m/%d/%Y')
            current_time = '{}:{}:{}'.format(
                '%02d' % selected_uss.created_at.hour,
                '%02d' % selected_uss.created_at.minute,
                '%02d' % selected_uss.created_at.second)

            for symptom in Symptom.objects.all():
                _symptom = dict(
                    id=symptom.id, name=symptom.name, disabled=False)
                try:
                    UserSingleSymptomSeverity.objects.get(
                        user_symptom_severities=selected_uss, symptom=symptom)

                    _symptom['disabled'] = True
                except ObjectDoesNotExist:
                    pass

                symptoms.append(_symptom)

            selected_uss = dict(
                id=selected_uss.id,
                title=selected_uss.title,
                date=selected_uss.created_at.strftime('%m/%d/%Y'),
                usss_list=[dict(
                    id=usss.id,
                    symptom=usss.getSymptom(),
                    level=usss.getLevel(),
                    description=usss.description
                ) for usss in selected_uss.getUSSSList()]
            )
        else:
            for symptom in Symptom.objects.all():
                _symptom = dict(
                    id=symptom.id, name=symptom.name, disabled=False)
                try:
                    CurrentUserSymptom.objects.get(user=user, symptom=symptom)

                    _symptom['disabled'] = True
                except ObjectDoesNotExist:
                    pass

                symptoms.append(_symptom)

        date_filter = None
        if 'date_filter' in kwargs:
            date_filter = kwargs['date_filter']

        org_symptoms = [dict(
            id=symptom.id,
            name=symptom.name,
            levels=symptom.getSymptomLevels()
        ) for symptom in Symptom.objects.all()]

        try:
            start_timestamp = datetime.strptime(
                '%s 00:00:00' % date_filter, '%m/%d/%Y %H:%M:%S')
            end_timestamp = datetime.strptime(
                '%s 23:59:59' % date_filter, '%m/%d/%Y %H:%M:%S')

            uss_list = [dict(
                id=uss.id,
                date=uss.created_at.strftime('%m/%d/%Y'),
                time=uss.created_at.strftime('%H:%M:%S'),
                title=uss.title
            ) for uss in UserSymptomSeverities.objects.filter(user=user, created_at__range=(start_timestamp, end_timestamp)).order_by('-created_at')]
        except:
            uss_list = [dict(
                id=uss.id,
                date=uss.created_at.strftime('%m/%d/%Y'),
                time=uss.created_at.strftime('%H:%M:%S'),
                title=uss.title
            ) for uss in UserSymptomSeverities.objects.filter(user=user).order_by('-created_at')]

        default_title = datetime.now().strftime('%m/%d Update')

        return render(request, self.template_name, dict(
            user_id=user_id,
            default_title=default_title,
            selected_uss=selected_uss,
            cus_list=cus_list,
            uss_list=uss_list,
            symptoms=symptoms,
            date_filter=date_filter,
            org_symptoms=org_symptoms,
            current_date=current_date,
            current_time=current_time
        ))
