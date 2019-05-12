from django import forms
from django.contrib import admin

# Register your models here.
from django.forms import BaseModelForm

from control.models import Departament, Student, Subject, Subdepartament, Group, Semester, Progress, Session


@admin.register(Departament)
class DepartamentAdmin(admin.ModelAdmin):
    search_fields = ['name', 'code']
    list_display = ('code', 'name')
    list_per_page = 10


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Subdepartament)
class SubdepartamentAdmin(admin.ModelAdmin):
    search_fields = ['name', 'code']
    list_display = ('code', 'name', 'departament')
    list_filter = ['departament']
    list_per_page = 10


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass

# class SemesterForm(BaseModelForm):
#     def __init__(self, *args, **kwargs):
#         super(BaseModelForm, self).__init__(*args, **kwargs)
#         username = forms.TextInput(attrs={'class': 'form-control'})
#
#     class Meta:
#         model = Semester
#         fields = ('name', 'code')

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    # add_form = SemesterForm
    # form = SemesterForm
    search_fields = ['name', 'code', 'session']
    list_display = ('name', 'code', 'session')
    list_filter = ['session']
    list_per_page = 10


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    pass


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    pass


# admin.site.register(Departament)
# admin.site.register(Student)
# admin.site.register(Subject)
# admin.site.register(Subdepartament)
# admin.site.register(Group)
# admin.site.register(Semester)
# admin.site.register(Progress)
# admin.site.register(Session)
