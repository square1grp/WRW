from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from wrw.models import User, Factor, CurrentIntermittentFactor, CurrentDailyFactor
from wrw.utils import isUserLoggedIn
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt


class UpdateFactorSeveritiesPage(View):
    template_name = 'pages/update-factor-severities.html'

    def get(self, request, *args, **kwargs):
        user_id = isUserLoggedIn(request)

        if not user_id:
            return HttpResponseRedirect('/')

        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return HttpResponse('No user.')

        current_time = dict(h='%02d' % datetime.now().hour,
                            m='%02d' % datetime.now().minute,
                            s='%02d' % datetime.now().second)

        cif_list = CurrentIntermittentFactor.objects.filter(
            user=user)
        cdf_list = CurrentDailyFactor.objects.filter(
            user=user)

        factors = []
        for factor in Factor.objects.all():
            _factor = dict(
                id=factor.id, title=factor.title, disabled=False)

            try:
                CurrentIntermittentFactor.objects.get(user=user, factor=factor)

                _factor['disabled'] = True
            except ObjectDoesNotExist:
                pass

            try:
                CurrentDailyFactor.objects.get(user=user, factor=factor)

                _factor['disabled'] = True
            except ObjectDoesNotExist:
                pass

            factors.append(_factor)

        org_factors = [dict(
            id=factor.id,
            title=factor.title,
            levels=factor.getFactorLevels()
        ) for factor in Factor.objects.all()]

        return render(request, self.template_name, dict(
            user_id=user_id,
            cif_list=cif_list,
            cdf_list=cdf_list,
            factors=factors,
            org_factors=org_factors,
            current_time=current_time
        ))
