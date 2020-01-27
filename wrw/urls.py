from django.urls import path, re_path

from .views.index import IndexPage
from .views.register import RegisterPage
from .views.verify import VerifyTokenPage

urlpatterns = [
    path('', IndexPage.as_view()),
    path('register/', RegisterPage.as_view()),
    re_path(r'register/verify-token/(?P<token>.*/)?$', VerifyTokenPage.as_view()),
]
