from django.urls import path, re_path

from django.views.decorators.csrf import csrf_exempt

from wrw.views.index import IndexPage
from wrw.views.register import RegisterPage
from wrw.views.account import AccountPage
from wrw.views.verify import VerifyTokenPage
from wrw.views.user import UserPage
from wrw.views.update_symptom_severities import UpdateSymptomSeveritiesPage
from wrw.views.update_factors import UpdateFactorsPage
from wrw.views.symptom import SymptomPage
from wrw.views.factor import FactorPage

urlpatterns = [
    path('', csrf_exempt(IndexPage.as_view())),
    path('register/', csrf_exempt(RegisterPage.as_view())),
    path('account/', csrf_exempt(AccountPage.as_view())),
    re_path(r'register/verify-token/(?P<token>.*/)?$',
            VerifyTokenPage.as_view()),
    path('user/<int:user_id>/', UserPage.as_view()),
    path('user/<int:user_id>/update_symptom_severities/',
         csrf_exempt(UpdateSymptomSeveritiesPage.as_view())),
    path('user/<int:user_id>/update_factors/',
         csrf_exempt(UpdateFactorsPage.as_view())),
    path('symptom/<int:symptom_id>/', SymptomPage.as_view()),
    path('symptom/<int:symptom_id>/factor/<int:factor_id>/', FactorPage.as_view()),
]
