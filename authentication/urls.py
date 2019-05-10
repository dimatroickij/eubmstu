from django.urls import path

from authentication import views

app_name = 'authentication'
urlpatterns = [
    path('accounts/registration/', views.registration, name='registration'),
    path('', views.profile, name='profile'),
    path('accounts/change', views.change, name='chenge'),
]
