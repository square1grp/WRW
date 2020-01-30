from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from wrw.models import User, Factor
from wrw.utils import isUserLoggedIn
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt


class UpdateFactorSeveritiesPage(View):
    template_name = 'pages/update-factor-severities.html'

    def get(self, request, *args, **kwargs):
        user_id = isUserLoggedIn(request)

        current_time = dict(h='%02d' % datetime.now().hour,
                            m='%02d' % datetime.now().minute,
                            s='%02d' % datetime.now().second)
        
        factors = Factor.objects.all()

        return render(request, self.template_name, dict(
            user_id=user_id,
            factors=factors,
            current_time=current_time
        ))
