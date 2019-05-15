"""eubmstu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from authentication.decorators import check_recaptcha
from authentication.forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm
from authentication.views import LoginView, PasswordResetView
from eubmstu import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/password_change/',
         auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html',
                                               form_class=MyPasswordChangeForm, success_url='/')),
    path('accounts/password_reset/',
         check_recaptcha(PasswordResetView.as_view())),
    path('accounts/login/',
         check_recaptcha(LoginView.as_view())),
    path('accounts/', include('django.contrib.auth.urls'), ),
    path('', include('authentication.urls'), ),
    path('', include('control.urls'), ),
    path('report/', include('report.urls'), ),
    path('favicon.ico', views.favicon),
]
