from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views import View
from wrw.utils import isUserLoggedIn
from wrw.models import Symptom, User
from statistics import mean


class SymptomPage(View):
    template_name = 'pages/symptom.html'

    def getUsersByFactorAndSymptom(self, symptom, factor):
        users = []

        for user in User.objects.all():
            factors = user.getFactorsBySymptom(symptom)

            if factor in factors:
                users.append(user)

        return users

    def getFaceClassName(self, score):
        if score > 60:
            return 'ecstatic-face'

        if score > 20:
            return 'happy-face'

        if score > -20:
            return 'neutral-face'

        if score > -60:
            return 'sad-face'

        return 'miserable-face'

    def getAvgSymptomScore(self, symptom, factor):
        scores = []

        for user in User.objects.all():
            severities = user.getSymptomSeverities(symptom, factor)

            if not severities:
                continue

            start_severity = severities[0] - 1
            end_severity = severities[-1] - 1

            actual = end_severity - start_severity
            max_pos = 4 - start_severity
            max_neg = 0 - start_severity

            score = (-100 * actual /
                     max_pos) if actual > 0 else (100 * actual/max_neg)

            scores.append(score)

        return round(mean(scores), 2)

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
        factors = []
        users = User.objects.all()
        for user in users:
            for factor in user.getFactorsBySymptom(symptom):
                if factor not in factors:
                    factors.append(factor)

        for factor in factors:
            score = self.getAvgSymptomScore(symptom, factor)
            rows.append(dict(
                factor=factor,
                score=score,
                face_class=self.getFaceClassName(score),
                user_count=len(
                    self.getUsersByFactorAndSymptom(symptom, factor))
            ))

        return render(request, self.template_name, dict(symptom=symptom, rows=rows))
