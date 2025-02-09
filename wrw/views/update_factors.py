from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views import View
from wrw.models import User, Factor, CurrentIntermittentFactor, UserFactors, UserIntermittentFactor, UserDailyFactorStart, UserDailyFactorEnd, UserDailyFactorMeta
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

    def updateUserDailyFactorMeta(self, udfs, selected_level, title, description, created_at, is_selected_uf=False):
        udfm = udfs.getTheLatestMeta()

        if udfm and selected_level:
            if is_selected_uf and udfm.created_at == created_at:
                udfm.selected_level = int(selected_level)
                udfm.title = title
                udfm.description = description

                udfm.save()

            if udfm.selected_level == int(selected_level):
                return

        udfm = UserDailyFactorMeta(
            user_daily_factor_start=udfs, selected_level=selected_level, title=title, description=description, created_at=created_at)

        udfm.save()

    def gefCurrentValues(self, user, params=dict()):
        current_date = datetime.now().strftime('%m/%d/%Y')
        current_time = '{}:{}:{}'.format('%02d' % datetime.now().hour,
                                         '%02d' % datetime.now().minute,
                                         '%02d' % datetime.now().second)

        if 'date' in params:
            current_date = params['date']
        if 'time' in params:
            current_time = params['time']

        created_at = datetime.strptime(
            '%s %s' % (current_date, current_time), '%m/%d/%Y %H:%M:%S')
        current_title = created_at.strftime('%m/%d Update')

        _udfs_list = [udfs for udfs in UserDailyFactorStart.objects.filter(
            user=user, created_at__lt=created_at) if not udfs.isEnded()]
        udfs_list = [dict(
            id=_udfs.id,
            factor=dict(
                id=_udfs.factor.id,
                title=_udfs.getFactorTitle(),
                levels=_udfs.getFactorLevels()),
            disabled=False
        ) for _udfs in _udfs_list]

        for factor in Factor.objects.all():
            udfs_last = UserDailyFactorStart.objects.filter(
                user=user, factor=factor, created_at__lt=created_at).order_by('-created_at').first()

            if udfs_last and udfs_last not in _udfs_list:
                if udfs_last.getEndedAt() and udfs_last.getEndedAt() > created_at:
                    udfs_list.append(dict(
                        id=udfs_last.id,
                        factor=dict(
                            id=udfs_last.factor.id,
                            title=udfs_last.getFactorTitle(),
                            levels=udfs_last.getFactorLevels()),
                        disabled=True
                    ))

        return [udfs_list, current_title, current_date, current_time]

    def getUFList(self, user, date_filter=None):
        if date_filter:
            start_timestamp = datetime.strptime(
                '%s 00:00:00' % date_filter, '%m/%d/%Y %H:%M:%S')
            end_timestamp = datetime.strptime(
                '%s 23:59:59' % date_filter, '%m/%d/%Y %H:%M:%S')

            uf_list = UserFactors.objects.filter(user=user, created_at__range=(
                start_timestamp, end_timestamp)).order_by('-created_at')
        else:
            uf_list = UserFactors.objects.filter(
                user=user).order_by('-created_at')

        return [dict(
            id=uf.id,
            date=uf.created_at.strftime('%m/%d/%Y'),
            time=uf.created_at.strftime('%H:%M:%S'),
            title=uf.title
        ) for uf in uf_list]

    def post(self, request, *args, **kwargs):
        user_id = isUserLoggedIn(request)

        if not user_id:
            return HttpResponseRedirect('/')

        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return HttpResponse('No user.')

        params = request.POST

        if params['action'] == 'get_daily_factors':
            [udfs_list, current_title, current_date,
                current_time] = self.gefCurrentValues(user, params)

            return JsonResponse(dict(
                udfs_list=udfs_list,
                current_title=current_title,
                current_date=current_date,
                current_time=current_time
            ))

        elif params['action'] == 'add':
            if 'selected_uf_id' in params:
                # update Update Factors
                uf = UserFactors.objects.get(
                    id=params['selected_uf_id'])

                # uf.created_at = datetime.strptime('%s %s' % (params['date'], params['time']), '%m/%d/%Y %H:%M:%S')
                uf.title = params['title']

                uf.save()

                uif_list = UserIntermittentFactor.objects.filter(
                    user_factors=uf)
                for uif in uif_list:
                    uif.delete()
            else:
                uf = self.createUserFactors(
                    user, params['date'], params['time'], params['title'])

            for factor_id in params.getlist('factor_Intermittent_IDs'):
                factor = Factor.objects.get(id=factor_id)

                description_key = 'factor_%s_description' % factor_id
                description = params[description_key] if description_key in params else ''

                selected_level_key = 'factor_%s_level' % factor_id
                selected_level = params[selected_level_key] if selected_level_key in params else None

                # create user intermittent factor
                self.createUserIntermittentFactor(
                    uf, factor, selected_level, description)

            for udfs_id in params.getlist('udfs_IDs'):
                udfs = UserDailyFactorStart.objects.get(id=udfs_id)

                title = params['title']

                description_key = 'udfs_%s_description' % udfs_id
                description = params[description_key] if description_key in params else ''

                selected_level_key = 'udfs_%s_level' % udfs_id
                selected_level = params[selected_level_key] if selected_level_key in params else None

                # create user daily factor meta
                self.updateUserDailyFactorMeta(
                    udfs, selected_level, title, description, uf.created_at, 'selected_uf_id' in params)

        elif params['action'] == 'delete':
            uf = UserFactors.objects.get(id=params['uf_id'])
            uf.delete()

        elif params['action'] == 'add_cif':
            factor_id = params['factor_id']

            cif = CurrentIntermittentFactor(
                user=user, factor=Factor.objects.get(id=factor_id))
            cif.save()

            return JsonResponse(dict(added=True, cif_id=cif.id))

        elif params['action'] == 'delete_cif':
            factor_id = params['factor_id']

            cif = CurrentIntermittentFactor.objects.get(
                user=user, factor__id=factor_id)
            cif.delete()

            return JsonResponse(dict(removed=True))

        elif params['action'] == 'add_udfs':
            factor_id = params['factor_id']
            factor = Factor.objects.get(id=factor_id)

            started_at = '%s %s' % (params['date'], params['time'])
            started_at = datetime.strptime(started_at, '%m/%d/%Y %H:%M:%S')

            udfs = UserDailyFactorStart(
                user=user, factor=factor, created_at=started_at)

            udfs.save()

            return JsonResponse(dict(
                added=True,
                udfs=dict(
                    id=udfs.id,
                    factor=dict(
                        id=udfs.factor.id,
                        title=udfs.getFactorTitle(),
                        levels=udfs.getFactorLevels()),
                    disabled=False)))

        elif params['action'] == 'add_udfe':
            udfs_id = params['udfs_id']

            started_at = '%s %s' % (params['date'], params['time'])
            started_at = datetime.strptime(started_at, '%m/%d/%Y %H:%M:%S')

            udfs = UserDailyFactorStart.objects.get(id=udfs_id)

            udfe = UserDailyFactorEnd(
                user_daily_factor_start=udfs, created_at=started_at)

            udfe.save()

            return JsonResponse(dict(removed=True))

        elif params['action'] == 'edit_uf':
            kwargs['uf_id'] = params['uf_id']

            if 'date_filter' in params:
                kwargs['date_filter'] = params['date_filter']

        elif params['action'] == 'get_uf_list':
            return JsonResponse(dict(uf_list=self.getUFList(user, params['date_filter'])))

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
            if params['action'] in ['convert-to-daily']:
                factor_id = params['factor_id']

                try:
                    cif = CurrentIntermittentFactor.objects.get(
                        user=user, factor__id=factor_id)
                    cif.delete()

                    if params['action'] == 'convert-to-daily':
                        factor_id = params['factor_id']

                        started_at = '%s %s' % (params['date'], params['time'])
                        started_at = datetime.strptime(
                            started_at, '%m/%d/%Y %H:%M:%S')

                        udfs = UserDailyFactorStart(
                            user=user, factor=Factor.objects.get(id=factor_id), created_at=started_at)

                        udfs.save()
                except:
                    pass

            elif params['action'] in ['convert-to-intermittent']:
                udfs_id = params['udfs_id']

                started_at = '%s %s' % (params['date'], params['time'])
                started_at = datetime.strptime(started_at, '%m/%d/%Y %H:%M:%S')

                try:
                    udfs = UserDailyFactorStart.objects.get(id=udfs_id)

                    udfe = UserDailyFactorEnd(
                        user_daily_factor_start=udfs, created_at=started_at)

                    udfe.save()

                    if params['action'] == 'convert-to-intermittent':
                        cif = CurrentIntermittentFactor(
                            user=user, factor=udfs.getFactor())
                        cif.save()
                except:
                    pass

            return HttpResponseRedirect('/user/%s/update_factors' % user_id)

        current_date = datetime.now().strftime('%m/%d/%Y')
        current_time = '{}:{}:{}'.format('%02d' % datetime.now().hour,
                                         '%02d' % datetime.now().minute,
                                         '%02d' % datetime.now().second)

        cif_list = CurrentIntermittentFactor.objects.filter(
            user=user)

        [udfs_list, current_title, current_date,
            current_time] = self.gefCurrentValues(user)

        selected_uf = None
        factors = []
        if 'uf_id' in kwargs:
            selected_uf = UserFactors.objects.get(
                id=kwargs['uf_id'])

            current_date = selected_uf.created_at.strftime('%m/%d/%Y')
            current_time = '{}:{}:{}'.format(
                '%02d' % selected_uf.created_at.hour,
                '%02d' % selected_uf.created_at.minute,
                '%02d' % selected_uf.created_at.second)

            for factor in Factor.objects.all():
                _factor = dict(
                    id=factor.id, title=factor.title, disabled=False)
                try:
                    UserIntermittentFactor.objects.get(
                        user_factors=selected_uf, factor=factor)

                    _factor['disabled'] = True
                except ObjectDoesNotExist:
                    pass

                factors.append(_factor)

            selected_uf = dict(
                id=selected_uf.id,
                title=selected_uf.title,
                uif_list=[dict(
                    id=uif.id,
                    factor=uif.getFactor(),
                    level=uif.getLevel(),
                    description=uif.description
                ) for uif in selected_uf.getUIFList()],
                udfs_list=[dict(
                    id=udfs.id,
                    factor=udfs.getFactor(),
                    level=udfs.getLevel(selected_uf.created_at),
                    description=udfs.getDescription()
                ) for udfs in selected_uf.getUDFSList()]
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

                if factor.id in [udfs['factor']['id'] for udfs in udfs_list]:
                    _factor['disabled'] = True

                factors.append(_factor)

        org_factors = [dict(
            id=factor.id,
            title=factor.title,
            levels=factor.getFactorLevels()
        ) for factor in Factor.objects.all()]

        date_filter = None
        if 'date_filter' in kwargs:
            date_filter = kwargs['date_filter']

        uf_list = self.getUFList(user, date_filter)

        return render(request, self.template_name, dict(
            user_id=user_id,
            cif_list=cif_list,
            udfs_list=udfs_list,
            factors=factors,
            selected_uf=selected_uf,
            uf_list=uf_list,
            org_factors=org_factors,
            date_filter=date_filter,
            current_title=current_title,
            current_date=current_date,
            current_time=current_time
        ))
