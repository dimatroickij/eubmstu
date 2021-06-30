from control.UpdateData import UpdateData
from control.models import Semester, Departament, Subdepartament, Group


def taskUpdateSemesters():
    ud = UpdateData()
    print('Обновление семестров')
    ud.updateSemesters()
    ud.eu.exit()


def taskUpdateDepartaments():
    ud = UpdateData()
    print('Обновление факультетов')
    ud.updateDepartaments()
    ud.eu.exit()


def taskUpdateSubDepartaments():
    ud = UpdateData()
    print('Обновление кафедр')
    ud.updateSubDepartaments()
    ud.eu.exit()


def taskUpdateGroups():
    ud = UpdateData()
    print('Обновление групп всех семестров')
    semesters = list(map(lambda x: x.pk, Semester.objects.all()))
    ud.updateGroups(semesters)
    ud.eu.exit()


def taskUpdateGroups():
    ud = UpdateData()
    print('Обновление БД студентов')
    ud.updateStudents()
    ud.eu.exit()


def taskUpdateStudentsAndProgressInGroup(i, code='ИУ6'):  # 23 - последний семестр (2018-02)
    ud = UpdateData()
    semester = Semester.objects.order_by('pk')[i]
    groups = Group.objects.filter(subdepartament__code=code, semester=semester)
    for group in groups:
        print('start %s' % group.name)
        print('updateSubjects')
        ud.updateSubjectsInGroup(group.code, semester.code)
        print('updateStudents')
        ud.updateStudentsInGroup(group.code, semester.code)
        print('updateProgress')
        ud.updateProgressInGroup(group.code, semester.code)
    ud.eu.exit()


# taskUpdateSessionIngroup(23)
def taskUpdateSessionIngroup(i, code='ИУ6'):  # 23 - последний семестр (2018-02)
    ud = UpdateData()
    semester = Semester.objects.order_by('pk')[i]
    groups = Group.objects.filter(subdepartament__code=code, semester=semester)
    isMain = True
    for i, group in enumerate(groups):
        print('start %s. %s/ %s' % (group.name, i + 1, len(groups)))
        ud.updateSessionInGroup(group.code, semester.code, isMain)
        if isMain:
            isMain = False
    ud.eu.exit()


def taskUpdateStudentsInGroup(sems, code='ИУ6'):  # 23 - последний семестр (2018-02)
    ud = UpdateData()
    for sem in sems:
        print('%s semester' % sem)
        semester = Semester.objects.order_by('pk')[sem]
        groups = Group.objects.filter(subdepartament__code=code, semester=semester)
        for i, group in enumerate(groups):
            print('start %s. %s/ %s' % (group.name, i + 1, len(groups)))
            ud.updateStudentsInGroup(group.code, semester.code)
    ud.eu.exit()


def taskUpdateStudentsBySubDep(countGroup):
    ud = UpdateData()
    subdepartaments = Subdepartament.objects.filter(prove=False)
    listGroups = []
    for subDep in subdepartaments:
        count = Group.objects.filter(subdepartament=subDep).count()
        if count != 0:
            listGroups.append({'subDep': subDep, 'count': count})
        else:
            print('%s', subDep.code)
            subDep.prove = True
            subDep.save()
    print('all count subDep: %s' % len(listGroups))
    listGroups = sorted(list(filter(lambda x: x['count'] <= countGroup, listGroups)), key=lambda x: x['count'])
    print('filter count subDep: %s' % len(listGroups))
    for i, subDep in enumerate(list(filter(lambda x: x['count'] <= countGroup, listGroups))):
        print('subDep: %s %s/%s' % (subDep['subDep'].code, i + 1, len(listGroups)))
        groups = Group.objects.filter(subdepartament=subDep['subDep'])
        for i, group in enumerate(groups):
            print('start %s. %s/ %s' % (group.name, i + 1, len(groups)))
            ud.updateStudentsInGroup(group.code, group.semester.code)
        subDep['subDep'].prove = True
        subDep['subDep'].save()
    ud.eu.exit()
