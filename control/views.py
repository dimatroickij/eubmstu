import os

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

from control.models import Subject, GroupSubject, Progress, Session
from eubmstu.settings import BASE_DIR


@login_required
def renameAndDeleteSubject(request):
    for subject in Subject.objects.all().order_by('pk'):
        print('%i - %s' % (subject.pk, subject.name))
        subject.name = subject.name.strip().replace('  ', ' ').replace('  ', '')
        try:
            subject.full_clean()
            subject.save()
        except ValidationError:
            lastSubject = Subject.objects.get(name=subject.name, subdepartament=subject.subdepartament)
            groupSubject1 = GroupSubject.objects.filter(subject=subject)
            for groupSubject in groupSubject1:
                print('## ##')
                groupSubject.subject = lastSubject
                try:
                    groupSubject.save()
                except IntegrityError:
                    lastGS = GroupSubject.objects.get(group=groupSubject.group, subject=lastSubject)
                    for pr in Progress.objects.filter(subject=groupSubject):
                        print('###  ###')
                        pr.subject = lastGS
                        try:
                            pr.save()
                        except IntegrityError:
                            lastPr = Progress.objects.get(subject=lastGS, student=pr.student)
                            if lastPr.point <= pr.point:
                                lastPr.point = pr.point
                            lastPr.save()
                            pr.delete()
                    for session in Session.objects.filter(subject=groupSubject):
                        print('*** ***')
                        session.subject = lastGS
                        try:
                            session.save()
                        except IntegrityError:
                            lastSession = Session.objects.get(subject=lastGS, student=session.student,
                                                              type_rating=session.type_rating)
                            if lastSession.rating == '' and session.rating != '':
                                lastSession.rating = session.rating
                            if lastSession.rating == 'НА' and session.rating != 'НА':
                                lastSession.rating = session.rating
                            if lastSession.rating == 'Нзч' and session.rating != 'Нзч':
                                lastSession.rating = session.rating
                            if lastSession.rating == 'Я' and session.rating != 'Я':
                                lastSession.rating = session.rating
                            if lastSession.rating == 'Напр' and session.rating != 'Напр':
                                lastSession.rating = session.rating
                            if lastSession.rating == 'Неуд' and session.rating != 'Неуд':
                                lastSession.rating = session.rating
                            if lastSession.rating == 'Дк' and session.rating != 'Дк':
                                lastSession.rating = session.rating
                            if lastSession.rating == 'П' and session.rating != 'П':
                                lastSession.rating = session.rating
                            if lastSession.rating == 'Д' and session.rating != 'Д':
                                lastSession.rating = session.rating
                            lastSession.save()
                            session.delete()
                    groupSubject.delete()
            subject.delete()
    return JsonResponse(1, safe=False)


@login_required
def faq(request):
    if request.user.is_superuser:
        return JsonResponse('FAQ superuser', safe=False)
    else:
        return JsonResponse('FAQ user', safe=False)
