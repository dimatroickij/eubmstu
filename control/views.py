import os

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

@login_required
def test(request):
    print(os.path.dirname(__file__))
    return JsonResponse('123', safe=False)