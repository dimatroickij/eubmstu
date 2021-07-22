from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse, JsonResponse, HttpResponse
from django.shortcuts import render
import csv
from django.core import serializers

from control.models import Semester, Departament, Subdepartament, Group


@login_required
def getSemesters(requests):
    return HttpResponse(serializers.serialize('json', Semester.objects.all().order_by('code')),
                        content_type='application/json')


@login_required
def getDepartaments(requests):
    return HttpResponse(serializers.serialize('json', Departament.objects.all().order_by('code')),
                        content_type='application/json')


@login_required
def getSubDepartaments(requests, departament):
    return HttpResponse(
        serializers.serialize('json', Subdepartament.objects.filter(departament=departament).order_by('code')),
        content_type='application/json')


@login_required
def getGroups(requests, semester, subdepartament):
    return HttpResponse(serializers.serialize('json', Group.objects.filter(semester=semester,
                                                                           subdepartament=subdepartament).order_by(
        'name')),
                        content_type='application/json')
