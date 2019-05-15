from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from authentication.forms import MyUserCreationForm, MyUserChangeForm, LoginForm, MyPasswordResetForm
from authentication.models import User


def registration(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = MyUserCreationForm(request.POST)
            if form.is_valid():
                if request.recaptcha_is_valid:
                    user = form.save()
                    user.is_active = False
                    user.save()
                    messages.add_message(request, messages.SUCCESS, 'Вы зарегистрированы. Ждите подтверждения.')
                return redirect('login')
        else:
            form = MyUserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})
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
    return redirect('profile')


from django.contrib.auth import views as auth_views, login


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'

    def form_valid(self, form):
        # проверка валидности reCAPTCHA
        if self.request.recaptcha_is_valid:
            login(self.request, form.get_user())
            return HttpResponseRedirect(self.get_success_url())
        return render(self.request, 'registration/login.html', self.get_context_data())


class PasswordResetView(auth_views.PasswordResetView):
    form_class = MyPasswordResetForm

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
        return render(self.request, 'registration/password_reset_form.html', self.get_context_data())
