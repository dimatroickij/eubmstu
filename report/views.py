from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
@login_required
def home(request):
    report = range(1, 9)
    return render(request,'report/home.html', {'report': report})