from django.urls import path

from report import views

app_name = 'report'
urlpatterns = [
    path('', views.home, name='home'),
    path('show/<int:group>/<int:code>', views.show, name='show'),
    path('students', views.students, name='students'),
    path('student/<int:id>', views.getStudent, name='getStudent'),
    path('group', views.group, name='group')
]
