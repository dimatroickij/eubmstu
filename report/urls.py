from django.urls import path

from report import views

app_name = 'report'
urlpatterns = [
    path('', views.home, name='home'),
    path('show/<int:code>', views.show, name='show')
]