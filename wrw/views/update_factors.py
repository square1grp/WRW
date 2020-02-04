from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from wrw.models import User, Factor, CurrentIntermittentFactor, CurrentDailyFactor, UserFactors, UserIntermittentFactor, UserDailyFactor, LevelTransition, SkippedDate
from wrw.utils import isUserLoggedIn
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist


class UpdateFactorsPage(View):
    template_name = 'pages/update-factors.html'

    def updateCIFs(self, user, factorIDs):
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

    def updateCDFs(self, user, factorIDs):
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

    def createUserFactors(self, user, date, time, title):
        created_at = datetime.strptime(
            '%s %s' % (date, time), '%m/%d/%Y %H:%M:%S')

        uf = UserFactors(
            user=user, title=title, created_at=created_at)
        uf.save()

        return uf

    def createUserIntermittentFactor(self, uf, factor, selected_level, description):
        uif = UserIntermittentFactor(
            user_factors=uf, factor=factor, selected_level=selected_level, description=description)

        uif.save()

    def createUserDailyFactor(self, uf, factor, selected_level, description):
        # create level transitions
        # skipped dates
        udf = UserDailyFactor(
            user_factors=uf, factor=factor, selected_level=selected_level, description=description)

        udf.save()

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
            if 'selected_uf_id' in params:
                # update Update Factors
                uf = UserFactors.objects.get(
                    id=params['selected_uf_id'])

                uf.created_at = datetime.strptime(
                    '%s %s' % (params['date'], params['time']), '%m/%d/%Y %H:%M:%S')
                uf.title = params['title']

                uf.save()

                uif_list = UserIntermittentFactor.objects.filter(
                    user_factors=uf)
                for uif in uif_list:
                    uif.delete()

                udf_list = UserDailyFactor.objects.filter(
                    user_factors=uf)
                for udf in udf_list:
                    udf.delete()
            else:
                # update Current Intermittent Factors
                self.updateCIFs(user, params.getlist(
                    'factor_Intermittent_IDs'))
                # update Current Daily Factors
                self.updateCDFs(user, params.getlist('factor_Daily_IDs'))

                uf = self.createUserFactors(
                    user, params['date'], params['time'], params['title'])

            for factor_id in params.getlist('factor_Intermittent_IDs'):
                factor = Factor.objects.get(id=factor_id)

                description_key = 'factor_%s_description' % factor_id
                description = params[description_key] if description_key in params else ''

                selected_level_key = 'factor_%s_level' % factor_id
                selected_level = params[selected_level_key] if selected_level_key in params else None

                self.createUserIntermittentFactor(
                    uf, factor, selected_level, description)

            for factor_id in params.getlist('factor_Daily_IDs'):
                factor = Factor.objects.get(id=factor_id)

                description_key = 'factor_%s_description' % factor_id
                description = params[description_key] if description_key in params else ''

                selected_level_key = 'factor_%s_level' % factor_id
                selected_level = params[selected_level_key] if selected_level_key in params else None

                self.createUserDailyFactor(
                    uf, factor, selected_level, description)

        elif params['action'] == 'delete':
            uf = UserFactors.objects.get(id=params['uf_id'])
            uf.delete()

        elif params['action'] in ['edit', 'date_filter']:
            if 'uf_id' in params:
                kwargs['uf_id'] = params['uf_id']

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

        current_time = dict(h='%02d' % datetime.now().hour,
                            m='%02d' % datetime.now().minute,
                            s='%02d' % datetime.now().second)

        cif_list = CurrentIntermittentFactor.objects.filter(
            user=user)
        cdf_list = CurrentDailyFactor.objects.filter(
            user=user)

        selected_uf = None
        factors = []
        if 'uf_id' in kwargs:
            selected_uf = UserFactors.objects.get(
                id=kwargs['uf_id'])

            current_time = dict(
                h='%02d' % selected_uf.created_at.hour,
                m='%02d' % selected_uf.created_at.minute,
                s='%02d' % selected_uf.created_at.second,
            )

            for factor in Factor.objects.all():
                _factor = dict(
                    id=factor.id, title=factor.title, disabled=False)
                try:
                    UserIntermittentFactor.objects.get(
                        user_factors=selected_uf, factor=factor)

                    _factor['disabled'] = True
                except ObjectDoesNotExist:
                    pass

                try:
                    UserDailyFactor.objects.get(
                        user_factors=selected_uf, factor=factor)

                    _factor['disabled'] = True
                except ObjectDoesNotExist:
                    pass

                factors.append(_factor)

            selected_uf = dict(
                id=selected_uf.id,
                title=selected_uf.title,
                date=selected_uf.created_at.strftime('%m/%d/%Y'),
                uif_list=[dict(
                    id=uif.id,
                    factor=uif.getFactor(),
                    level=uif.getLevel(),
                    description=uif.description
                ) for uif in selected_uf.getUIFList()],
                udf_list=[dict(
                    id=udf.id,
                    factor=udf.getFactor(),
                    level=udf.getLevel(),
                    description=udf.description
                ) for udf in selected_uf.getUDFList()]
            )
        else:
            for factor in Factor.objects.all():
                _factor = dict(
                    id=factor.id, title=factor.title, disabled=False)

                try:
                    CurrentIntermittentFactor.objects.get(
                        user=user, factor=factor)

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

        date_filter = datetime.now().strftime('%m/%d/%Y')
        if 'date_filter' in kwargs:
            date_filter = kwargs['date_filter']

        uf_list = [dict(
            id=uf.id,
            date=uf.created_at.strftime('%m/%d/%Y'),
            time=uf.created_at.strftime('%H:%M:%S'),
            title=uf.title
        ) for uf in UserFactors.objects.filter(
            user=user,
            created_at__range=(datetime.strptime('%s 00:00:00' % date_filter, '%m/%d/%Y %H:%M:%S'),
                               datetime.strptime('%s 23:59:59' % date_filter, '%m/%d/%Y %H:%M:%S'))
        ).order_by('-created_at')]

        return render(request, self.template_name, dict(
            user_id=user_id,
            cif_list=cif_list,
            cdf_list=cdf_list,
            factors=factors,
            selected_uf=selected_uf,
            uf_list=uf_list,
            org_factors=org_factors,
            date_filter=date_filter,
            current_time=current_time
        ))
