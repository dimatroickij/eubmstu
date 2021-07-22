from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from control.models import Progress, Group, Session, GroupSubject, Student, Semester, Departament
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
    form = StudentsFilterForm(request.GET)
    sort = 'last_name'
    search = ''
    iexact = ''
    listStudents = []
    if form.is_valid():
        print("#" + form.cleaned_data["search"] + "#")
        z = form.cleaned_data["search"]
        if form.cleaned_data["search"] and form.cleaned_data["search"] != '':
            try:
                if form.cleaned_data["iexact"]:
                    listStudents = Student.objects.filter(last_name__iexact=form.cleaned_data["search"].lower()) | \
                                   Student.objects.all().filter(first_name__iexact=form.cleaned_data["search"].lower())
                    iexact = 'on'
                else:
                    listStudents = Student.objects.all().filter(
                        last_name__icontains=form.cleaned_data["search"].lower()) | Student.objects.all().filter(
                        first_name__icontains=form.cleaned_data["search"].lower())
                search = form.cleaned_data["search"]
            except Student.DoesNotExist:
                pass
            if form.cleaned_data["ordering"]:
                listStudents = listStudents.order_by(form.cleaned_data["ordering"])
                sort = form.cleaned_data["ordering"]
            for student in listStudents:
                student.group = Group.objects.filter(students=student).order_by('semester')
    paginator = Paginator(listStudents, 10)
    page = request.GET.get('page')
    studentsPaginator = paginator.get_page(page)
    return render(request, 'report/students.html',
                  {'students': studentsPaginator, 'studentsSize': len(listStudents), 'form': form, 'ordering': sort,
                   'search': search, 'iexact': iexact}, )


def getColor(rating):
    if rating == 'Дк' or rating == 'Дисциплина' or rating == 'Подготовка':
        return 'bg-light text-dark'
    if rating == 'Нзч' or rating == 'НА' or rating == 'Я' or rating == 'Напр' or rating == 'Неуд':
        return 'bg-danger text-light'
    if rating == 'Удов':
        return 'bg-warning text-dark'
    if rating == 'Отл' or rating == 'Зчт':
        return 'bg-success text-light'
    if rating == 'Хор':
        return 'bg-info text-dark'
    return 'bg-secondary text-light'


def formatResult(student, subject):
    name = subject.subject.name
    progress = Progress.objects.filter(student__pk=student, subject=subject)
    point = '' if not progress.exists() else progress[0].point
    session = Session.objects.filter(student=student, subject=subject)
    subDep = subject.subject.subdepartament.code
    rating = list(
        map(lambda x: {'point': x.rating, 'color': getColor(x.rating), 'type_rating': x.get_type_rating_display()},
            session))
    return {'name': name, 'point': point, 'rating': rating, 'subDep': subDep}


@login_required
def getStudent(request, id):
    student = Student.objects.get(pk=id)
    groups = list(map(lambda x: {'pk': x.pk, 'name': x.name, 'semester': x.semester.name,
                                 'results': list(
                                     map(lambda y: formatResult(id, y), GroupSubject.objects.filter(group=x)))},
                      Group.objects.filter(students=student).order_by('semester')))
    return render(request, 'report/student.html', {'student': student, 'groups': groups})


@login_required
def group(request):
    semesters = Semester.objects.all().order_by('code')
    departaments = Departament.objects.all().order_by('code')
    return render(request, 'report/group.html', {'semesters': semesters, 'departaments': departaments})
