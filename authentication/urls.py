from django.urls import path

from authentication import views
from authentication.decorators import check_recaptcha

app_name = 'authentication'
urlpatterns = [
    path('accounts/registration/', check_recaptcha(views.registration), name='registration'),
    path('', views.profile, name='profile'),
    path('accounts/change', views.change, name='chenge'),
]
