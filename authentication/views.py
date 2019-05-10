from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from authentication.forms import MyUserCreationForm, MyUserChangeForm
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
