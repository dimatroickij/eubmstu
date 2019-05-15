from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from authentication.forms import MyUserCreationForm, MyUserChangeForm, LoginForm
from authentication.models import User


def registration(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = MyUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.is_active = False
                user.save()
                messages.add_message(request, messages.SUCCESS, 'Вы зарегистрированы. Ждите подтверждения.')
                return JsonResponse('122', safe=False)
        else:
            form = MyUserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})
    else:
        return redirect('profile')

def profile(request):
    if request.user.is_authenticated:

        return render(request, 'registration/profile.html', {})
    else:
        return redirect('login')

def change(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = MyUserChangeForm(request.POST, instance=user)
            if form.is_valid():
                user = form.save()
                user.is_active = False
                user.save()
                messages.add_message(request, messages.SUCCESS, 'Данные успешно изменены')
                return redirect('profile')
        else:
            form = MyUserChangeForm(instance=user)
        return render(request, 'registration/changeProfile.html', {'form': form})
    else:
        return redirect('login')

from django.contrib.auth import views as auth_views, login


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'

    def form_valid(self, form):
        # проверка валидности reCAPTCHA
        if self.request.recaptcha_is_valid:
            login(self.request, form.get_user())
            return HttpResponseRedirect(self.get_success_url())
        return render(self.request, 'registration/login.html', self.get_context_data(), {'errorCaptcha': 'is_invalid'})