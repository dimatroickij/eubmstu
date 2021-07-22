from django.urls import path

from api import views

app_name = 'api'
urlpatterns = [
    path('semesters', views.getSemesters, name='getSemesters'),
    path('departaments', views.getDepartaments, name='getDepartaments'),
    path('subdepartaments/<int:departament>', views.getSubDepartaments, name='getSubDepartaments'),
    path('groups/<int:semester>/<int:subdepartament>', views.getGroups, name='getGroups')
]
