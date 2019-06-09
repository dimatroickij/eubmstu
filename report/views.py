from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from control.models import Progress, Group, Session, GroupSubject


@login_required
def home(request):
    report = range(1, 7)
    return render(request, 'report/home.html', {'report': report})


@login_required
def show(request, code):
    group = Group.objects.get(pk=28519)
    students = group.students.all()
    if code == 1:
        reports = Progress.objects.filter(student__in=students, subject__group=group)
    else:
        reports = Session.objects.filter(student__in=students, subject__group=group)
    subjects = sorted(list(map(lambda x: {'subject': GroupSubject.objects.get(pk=x['subject']).subject.name,
                                          'subDep': GroupSubject.objects.get(pk=x['subject']).subject.subdepartament},
                               reports.filter(student=students[0]).values('subject'))), key=lambda x: x['subject'])
    mass = []
    if code == 1:
        for student in students:
            mass.append({'student': student, 'progress': sorted(
                list(map(lambda x: {'subject': x.subject.subject.name, 'point': x.point},
                         reports.filter(student=student))),
                key=lambda x: x['subject'])})
    else:
        for student in students:
            mass.append({'student': student, 'progress': sorted(
                list(map(lambda x: {'subject': x.subject.subject.name, 'point': x.rating},
                         reports.filter(student=student))),
                key=lambda x: x['subject'])})
    return render(request, 'report/show.html', {'group': group.name,
                                                'reports': sorted(mass, key=lambda x: x['student'].last_name),
                                                'subjects': subjects,
                                                'semester': group.semester.name})
