import os

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from eubmstu.settings import BASE_DIR


@login_required
def test(request):
    print(os.environ)
    return JsonResponse(1, safe=False)

@login_required
def faq(request):
    if request.user.is_superuser:
        return JsonResponse('FAQ superuser', safe=False)
    else:
        return JsonResponse('FAQ user', safe=False)