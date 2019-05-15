from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from authentication.forms import MyUserCreationForm, MyUserChangeForm, LoginForm, MyPasswordResetForm
from authentication.models import User
import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator


def registration(request):
    is_valid = True
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = MyUserCreationForm(request.POST)
            if form.is_valid():
                if request.recaptcha_is_valid:
                    user = form.save()
                    user.is_active = False
                    user.is_staff = False
                    user.save()
                    messages.add_message(request, messages.SUCCESS, 'Вы зарегистрированы. Ждите подтверждения.')
                    return redirect('login')
                else:
                    is_valid = False
        else:
            form = MyUserCreationForm()
        return render(request, 'registration/signup.html', {'form': form, 'is_valid': is_valid})
    return redirect('profile')


@login_required
def profile(request):
    if request.user.is_authenticated:
        form = MyUserChangeForm(instance=request.user)
        return render(request, 'registration/profile.html', {'form': form})


@login_required
def change(request):
    user = request.user
    if request.method == 'POST':
        form = MyUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Данные успешно изменены')
    return redirect('authentication:profile')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        print(User is None)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    print(account_activation_token.check_token(user, token))
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.add_message(request, messages.SUCCESS, 'Email подтверждён. Выполнен вход на сайт.')
    else:
        messages.add_message(request, messages.SUCCESS, 'Ошибка подтверждения email')
    return redirect('authentication:profile')
#localhost:8000/activate/Mw/56c-30a39db3df71891bfb5b

from django.contrib.auth import views as auth_views, login


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    extra_context = {'is_valid': True}

    def form_valid(self, form):
        # проверка валидности reCAPTCHA
        if self.request.recaptcha_is_valid:
            login(self.request, form.get_user())
            return HttpResponseRedirect(self.get_success_url())
        else:
            self.extra_context = {'is_valid': False}
        return render(self.request, 'registration/login.html', self.get_context_data(), )


class PasswordResetView(auth_views.PasswordResetView):
    form_class = MyPasswordResetForm
    extra_context = {'is_valid': True}

    def form_valid(self, form):
        if self.request.recaptcha_is_valid:
            opts = {
                'use_https': self.request.is_secure(),
                'token_generator': self.token_generator,
                'from_email': self.from_email,
                'email_template_name': self.email_template_name,
                'subject_template_name': self.subject_template_name,
                'request': self.request,
                'html_email_template_name': self.html_email_template_name,
                'extra_email_context': self.extra_email_context,
            }
            form.save(**opts)
            return super().form_valid(form)
        else:
            self.extra_context = {'is_valid': False}
        return render(self.request, 'registration/password_reset_form.html', self.get_context_data())


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()
