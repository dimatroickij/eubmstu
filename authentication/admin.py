from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from authentication.forms import MyUserCreationForm, UserChangeForm, MyUserChangeForm
from authentication.models import User


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('username', 'last_name', 'first_name', 'patronymic', 'is_active', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'email')}),
        ('Персональная информация', {'fields': ('last_name', 'first_name', 'patronymic')}),
        ('Права доступа', {'fields': ('is_active', 'is_superuser')}),
        # ('Важные даты', {'fields': ('date_joined', 'last_login')}),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'email')}),
        ('Пароль', {'fields': ('password1', 'password2')}),
        ('Персональная информация', {'fields': ('last_name', 'first_name', 'patronymic')}),
        ('Права доступа', {'fields': ('is_active', 'is_superuser')}),
    )

    search_fields = ['username', 'last_name', 'first_name', 'is_active']
    list_filter = ['is_active', 'is_superuser']

admin.site.register(User, MyUserAdmin)
admin.site.unregister(Group)