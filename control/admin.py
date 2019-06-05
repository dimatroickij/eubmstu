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
    search_fields = ['first_name', 'last_name', 'patronymic', 'gradebook']
    list_display = ('last_name', 'first_name', 'patronymic', 'gradebook', 'isStudying')
    list_filter = ['isStudying']
    list_per_page = 10


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    search_fields = ['name', 'subdepartament']
    list_display = ('name', 'subdepartament')
    list_filter = ['subdepartament']
    list_per_page = 10


@admin.register(Subdepartament)
class SubdepartamentAdmin(admin.ModelAdmin):
    search_fields = ['name', 'code']
    list_display = ('code', 'name', 'departament')
    list_filter = ['departament']
    list_per_page = 10


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    search_fields = ['name', 'code']
    list_display = ('name', 'code')
    list_filter = ['isEmpty', 'semester', 'subdepartament', 'levelEducation']
    list_per_page = 10


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    search_fields = ['name', 'code']
    list_display = ('name', 'code')
    list_per_page = 10


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'point')
    list_per_page = 10


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    pass
