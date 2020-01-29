from django.urls import path, re_path

from wrw.views.index import IndexPage
from wrw.views.register import RegisterPage
from wrw.views.verify import VerifyTokenPage
from wrw.views.user import UserPage
from wrw.views.update_symptom_severities import UpdateSymptomSeveritiesPage

urlpatterns = [
    path('', IndexPage.as_view()),
    path('register/', RegisterPage.as_view()),
    re_path(r'register/verify-token/(?P<token>.*/)?$',
            VerifyTokenPage.as_view()),
    path('user/<int:user_id>/', UserPage.as_view()),
    path('user/<int:user_id>/update_symptom_severities/',
         UpdateSymptomSeveritiesPage.as_view()),
]
