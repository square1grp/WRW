from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from datetime import datetime
from wrw.models import User
from uuid import uuid4
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from wrw.utils import isUserLoggedIn, gernerateUserToken
from website.settings import SENDGRID_KEY, GOOGLE_MAP_KEY


class AccountPage(View):
    template_name = 'pages/account.html'

    def getEthnicityList(self):
        return {
            'American', 'Indian', 'Asian', 'Black', 'Native Hawaiian', 'White', 'Hispanic', 'Prefer Not to Say'
        }

    def post(self, request, *args, **kwargs):
        params = request.POST
        user_id = isUserLoggedIn(request)

        if not user_id:
            return HttpResponseRedirect('/')

        user = User.objects.get(id=user_id)

        if params['action'] == 'change_password':
            if user.password == params['old_password']:
                user.password = params['new_password']
                kwargs['password_changed'] = True
            else:
                kwargs['wrong_password'] = True

            token = gernerateUserToken(user)

            request.session['wrw_token'] = token

            user.save()

        elif params['action'] == 'change_email':
            confirm_token = str(uuid4())

            user.email_to_confirm = params['new_email']
            user.confirm_token = confirm_token

            href = 'http://127.0.0.1:8000/register/verify-token/%s' % confirm_token

            message = Mail(
                from_email='info@whatreallyworks.com',
                to_emails=params['new_email'],
                subject='Email verification',
                html_content='<a href="%s" target="_blank">Click here</a> or visit this URL on the browser: %s' % (href, href))

            sg = SendGridAPIClient(SENDGRID_KEY)
            sg.send(message)

            kwargs['email_confirmation'] = True

            user.save()

        elif params['action'] == 'change_profile':
            user.birth_year = params['birth_year']
            user.ethnicity_top = params['ethnicity_top']
            user.ethnicity_second = params['ethnicity_second']
            user.ethnicity_third = params['ethnicity_third']
            user.gender = params['gender']
            user.sexual_orientation = params['sexual_orientation']
            user.city = params['city']
            user.state = params['state']
            user.country = params['country']

            kwargs['profile_is_changed'] = True

            user.save()

        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user_id = isUserLoggedIn(request)

        if not user_id:
            return HttpResponseRedirect('/')

        user = User.objects.get(id=user_id)

        years = [r for r in range(1900, datetime.today().year+1)]
        years.reverse()

        ethnicity_list = self.getEthnicityList()

        wrong_password = True if 'wrong_password' in kwargs else False
        password_changed = True if 'password_changed' in kwargs else False
        email_confirmation = True if 'email_confirmation' in kwargs else False
        profile_is_changed = True if 'profile_is_changed' in kwargs else False
        return render(
            request,
            self.template_name,
            dict(
                user=user,
                years=years,
                ethnicity_list=ethnicity_list,
                profile_is_changed=profile_is_changed,
                email_confirmation=email_confirmation,
                password_changed=password_changed,
                wrong_password=wrong_password,
                GOOGLE_MAP_KEY=GOOGLE_MAP_KEY)
        )
