from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from control.models import Progress, Group, Subject


@login_required
def home(request):
    report = range(1, 7)
    return render(request, 'report/home.html', {'report': report})


def show(request, code):
    students = Group.objects.get(pk=28519).students.all()
    reports = Progress.objects.filter(student__in=students)
    subjects = sorted(list(map(lambda x: {'subject': Subject.objects.get(pk=x['subject']).name,
                                          'subDep': Subject.objects.get(pk=x['subject']).subdepartament},
                               reports.filter(student=students[0]).values('subject'))), key=lambda x: x['subject'])
    mass = []
    for student in students:
        mass.append({'student': student, 'progress': sorted(
            list(map(lambda x: {'subject': x.subject.subject.name, 'point': x.point}, reports.filter(student=student))),
            key=lambda x: x['subject'])})
    return render(request, 'report/show.html', {'group': Group.objects.get(pk=28519).name,
                                                'reports': sorted(mass, key=lambda x: x['student'].last_name),
                                                'subjects': subjects,
                                                'semester': Group.objects.get(pk=28519).semester.name})
