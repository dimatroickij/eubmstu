from django.contrib import admin

# Register your models here.

from control.models import Departament, Student, Subject, Subdepartament, Group, Semester, Progress, Session


@admin.register(Departament)
class DepartamentAdmin(admin.ModelAdmin):
    pass


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Subdepartament)
class SubdepartamentAdmin(admin.ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    pass


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
