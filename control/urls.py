from django.urls import path

from control import views

app_name = 'control'
urlpatterns = [
    path('test', views.test, name='test'),
]