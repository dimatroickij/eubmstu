from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from authentication.forms import MyUserCreationForm


def registration(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = MyUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.is_active = False
                user.save()
                messages.add_message(request, messages.SUCCESS, 'Подтвердите email для завершения регистрации')
                return JsonResponse('122', safe=False)
        else:
            form = MyUserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})
    else:
        return render(request, 'registration/signup.html', )


def home(request):
    # if not request.user.is_authenticated:
    return render(request, 'registration/home.html', {})
    # else:
    #     return JsonResponse('registration')
