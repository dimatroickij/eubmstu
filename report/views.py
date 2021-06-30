from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from control.models import Progress, Group, Session, GroupSubject, Student
from report.forms import StudentsFilterForm


@login_required
def home(request):
    report = range(1, 7)
    return render(request, 'report/home.html', {'report': report})


@login_required
def show(request, group, code):
    group = Group.objects.get(pk=group)
    students = group.students.all()
    mass = []
    if len(students) != 0:
        if code == 1:
            reports = Progress.objects.filter(student__in=students, subject__group=group)
        else:
            reports = Session.objects.filter(student__in=students, subject__group=group)
        i = 0
        while reports.filter(student=students[i]).count() == 0:
            i += 1
        subjects = sorted(list(map(lambda x: {'subject': GroupSubject.objects.get(pk=x['subject']).subject.name,
                                              'subDep': GroupSubject.objects.get(
                                                  pk=x['subject']).subject.subdepartament},
                                   reports.filter(student=students[i]).values('subject'))), key=lambda x: x['subject'])
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
    else:
        subjects = []
    return render(request, 'report/show.html', {'group': group.name,
                                                'reports': sorted(mass, key=lambda x: x['student'].last_name),
                                                'subjects': subjects,
                                                'semester': group.semester.name})

@login_required
def students(request):
    students = Student.objects.all()
    form = StudentsFilterForm(request.GET)
    sort = 'last_name'
    search = ''
    iexact = ''
    if form.is_valid():
        print("#" + form.cleaned_data["search"] + "#")
        if form.cleaned_data["search"] and form.cleaned_data["search"] != None:
            try:
                if form.cleaned_data["iexact"]:
                    students = students.filter(last_name__iexact=form.cleaned_data["search"].lower()) | \
                               students.filter(first_name__iexact=form.cleaned_data["search"].lower())
                    iexact = 'on'
                else:
                    students = students.filter(last_name__icontains=form.cleaned_data["search"].lower()) | \
                               students.filter(first_name__icontains=form.cleaned_data["search"].lower())
                search = form.cleaned_data["search"]
            except Student.DoesNotExist:
                pass
        if form.cleaned_data["ordering"]:
            students = students.order_by(form.cleaned_data["ordering"])
            sort = form.cleaned_data["ordering"]
    for student in students:
         student.group = Group.objects.filter(students=student).order_by('semester')
    paginator = Paginator(students, 10)
    page = request.GET.get('page')
    stusentsPaginator = paginator.get_page(page)
    return render(request, 'report/students.html',
                  {'students': stusentsPaginator, 'studentsSize': students.count(), 'form': form, 'ordering': sort,
                   'search': search, 'iexact': iexact}, )

@login_required
def student(request, id):
    student = Student.objects.get(pk=id)
    return render(request, 'report/student.html',
                  {'student': student, 'groups': Group.objects.filter(students=student).order_by('semester')})