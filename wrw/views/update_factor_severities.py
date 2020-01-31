from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from wrw.models import User, Factor, CurrentIntermittentFactor, CurrentDailyFactor
from wrw.utils import isUserLoggedIn
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist


class UpdateFactorSeveritiesPage(View):
    template_name = 'pages/update-factor-severities.html'

    def updateCIFSs(self, user, factorIDs):
        factors = Factor.objects.filter(id__in=factorIDs)

        cif_list = CurrentIntermittentFactor.objects.filter(
            user=user).exclude(factor__id__in=factorIDs)

        for cif in cif_list:
            cif.delete()

        for factor in factors:
            try:
                CurrentIntermittentFactor.objects.get(user=user, factor=factor)
            except ObjectDoesNotExist:
                cif = CurrentIntermittentFactor(user=user, factor=factor)
                cif.save()

    def updateCDFS(self, user, factorIDs):
        factors = Factor.objects.filter(id__in=factorIDs)

        cdf_list = CurrentDailyFactor.objects.filter(
            user=user).exclude(factor__id__in=factorIDs)

        for cdf in cdf_list:
            cdf.delete()

        for factor in factors:
            try:
                CurrentDailyFactor.objects.get(user=user, factor=factor)
            except ObjectDoesNotExist:
                cdf = CurrentDailyFactor(user=user, factor=factor)
                cdf.save()

    def post(self, request, *args, **kwargs):
        user_id = isUserLoggedIn(request)

        if not user_id:
            return HttpResponseRedirect('/')

        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return HttpResponse('No user.')

        params = request.POST

        import pdb
        pdb.set_trace()

        if params['action'] == 'add':
            self.updateCIFSs(user, params.getlist('factor_Intermittent_IDs'))
            self.updateCDFS(user, params.getlist('factor_Daily_IDs'))
            pass

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
