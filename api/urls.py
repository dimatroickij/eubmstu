from django.urls import path

from api import views

app_name = 'api'
urlpatterns = [
    path('semesters', views.getSemesters, name='getSemesters')
]
