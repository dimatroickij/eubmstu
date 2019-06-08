from django.core.exceptions import ValidationError
from psycopg2._psycopg import OperationalError

from control.GetDataEU import GetDataEU
from control.models import Semester, Departament, Subdepartament, Group, Student, Subject, Progress, GroupSubject, \
    Session
from eubmstu.exceptions import EmptyListDeps, EmptyListSubDeps, EmptyListGroups, SubDepsNotFound
from eubmstu.settings import USERNAME, PASSWORD


class UpdateData:

    def __init__(self):
        self.eu = GetDataEU(USERNAME, PASSWORD, False, True)
        self.eu.login()

    # 7 секунд
    def updateSemesters(self):
        try:
            semesters = self.eu.getSemesters()
            for semester in semesters:
                try:
                    save = Semester(name=semester['name'], code=semester['link'])
                    save.full_clean()
                    save.save()
                except ValidationError:
                    pass
            return True
        except Exception as err:
            return err

    # 9 секунд
    def updateDepartaments(self):
        try:
            departaments = self.eu.getDepartaments()
            for departament in departaments:
                try:
                    save = Departament(name=departament['name'], code=departament['code'])
                    save.full_clean()
                    save.save()
                except ValidationError:
                    pass
            return True
        except Exception as err:
            return err

    # 38 секунд
    def updateSubDepartaments(self):
        try:
            departaments = Departament.objects.exclude(code='АДМИН').order_by('code')
            for dep in departaments:
                subDeps = self.eu.getSubDepartaments(dep.code)
                for subDep in subDeps:
                    try:
                        save = Subdepartament(name=subDep['name'], code=subDep['code'], departament=dep)
                        save.full_clean()
                        save.save()
                    except ValidationError:
                        pass
            return True
        except Exception as err:
            return err

    def updateGroups(self, sems):
        try:
            semesters = Semester.objects.filter(pk__in=sems)
            for semester in semesters:
                print(semester.name)
                try:
                    subDeps = Subdepartament.objects.exclude(departament__code='АДМИН')
                    for subDep in subDeps:
                        try:
                            groups = self.eu.getGroups(subDep.departament.code, subDep.code, semester.code)
                            for group in groups:
                                if group['isEmpty'] == '':
                                    isEmpty = False
                                else:
                                    isEmpty = True
                                record = Group(name=group['name'], code=group['code'], semester=semester,
                                               subdepartament=subDep,
                                               levelEducation=group['levelEducation'], isEmpty=isEmpty)
                                try:
                                    record.full_clean()
                                    record.save()
                                except ValidationError:
                                    pass
                        except SubDepsNotFound:
                            pass
                        except EmptyListSubDeps:
                            subDeps = subDeps.exclude(departament=subDep.departament)
                except EmptyListDeps:
                    pass
            return True
        except OperationalError:
            print('Ошибка базы данных')
        except Exception as err:
            return err

    def updateStudents(self, listDep):
        try:
            listLinkDeps = self.eu.getLinkDeps()
            for number in listDep:
                count = self.eu.getCountStudentsDep(listLinkDeps[number]['link'])
                print(listLinkDeps[number]['dep'] + ' ' + str(count))
                for num in range(1, count + 1):
                    print(str(num) + '/' + str(count))
                    student = self.eu.getStudentDep(listLinkDeps[number]['link'], num)
                    try:
                        find = Student.objects.get(gradebook=student['gradebook'])
                        z = find.gradebook
                        # proveStudentInGroup(find, student['group'], Semester.objects.all().last().id)
                    except Student.DoesNotExist:
                        name = student['name'].split(' ')
                        if len(name) == 2:
                            name.append('')
                        stud = Student(last_name=name[0], first_name=name[1], patronymic=name[2],
                                       gradebook=student['gradebook'])
                        stud.save()
                        # proveStudentInGroup(stud, student['group'], Semester.objects.all().last().id)
        except Exception as err:
            return err

    def updateSubjectsInGroup(self, groupCode, semester):
        group = Group.objects.get(code=groupCode)
        try:
            listSubjects = self.eu.getProgressInGroup(groupCode, semester, True, False, False)
            for subject in listSubjects['subjects']:
                try:
                    find = Subject.objects.get(name=subject['subject'],
                                               subdepartament=Subdepartament.objects.get(code=subject['subDep']))
                    try:
                        GroupSubject.objects.get(group=group, subject=find).group
                    except GroupSubject.DoesNotExist:
                        GroupSubject(group=group, subject=find).save()
                    # find.groups.add(group)
                    # find.save()
                except Subject.DoesNotExist:
                    newRecord = Subject(name=subject['subject'],
                                        subdepartament=Subdepartament.objects.get(code=subject['subDep']))
                    newRecord.save()
                    try:
                        GroupSubject.objects.get(group=group, subject=newRecord).group
                    except GroupSubject.DoesNotExist:
                        GroupSubject(group=group, subject=newRecord).save()
                    # newRecord.groups.add(group)
                    # newRecord.save()
            return True
        except Exception as err:
            return err

    def updateStudentsInGroup(self, code, semester):
        group = Group.objects.get(code=code, semester__code=semester)
        try:
            # добавить проверку на то, что студент может перевестись в другую группу и в этой его нужно удалить
            newListStudents = self.eu.getProgressInGroup(code, semester, False, True, False)
            for student in newListStudents['students']:
                find = Student.objects.get(last_name=student['student'], gradebook=student['gradeBook'])
                if Group.objects.filter(students=find, semester__code=semester).exclude(pk=group.pk).count() != 0:
                    lastGroup = Group.objects.get(students=find, semester__code=semester)
                    lastGroup.students.remove(find)
                group.students.add(find)
            return True
        except Exception as err:
            return err

    def updateProgressInGroup(self, code, semester):
        group = Group.objects.get(code=code, semester__code=semester)
        try:
            listProgress = self.eu.getProgressInGroup(code, semester, False, False, True)
            students = group.students.all().order_by('last_name', 'first_name', 'patronymic')
            for i, progress in enumerate(listProgress['progress']):
                for cell in progress:
                    subject = GroupSubject.objects.filter(group=group).get(subject__name=cell['subject'])
                    try:
                        record = Progress(subject=subject, student=students[i], point=cell['point'])
                        record.full_clean()
                        record.save()
                    except ValidationError:
                        record = Progress.objects.get(subject=subject, student=students[i])
                        record.point = cell['point']
                        record.save()
            return True
        except Exception as err:
            return err

    # 1.24 минуты - 19 человек, 7 предметов
    # 57 секунд - 17 человек, 7 предметов
    # 1.05 - 20 человек, 7 предметов
    # 30 сек - 4 человека, 7 предметов
    def updateSessionInGroup(self, code, semester):
        group = Group.objects.get(code=code, semester__code=semester)
        try:
            response = self.eu.getSessionInGroup(code, group.semester.pk + 3)
            listSubject = []
            for subject in response['subjects']:
                try:
                    listSubject.append(
                        {'subject': GroupSubject.objects.get(group=group, subject__name=subject['subject']),
                         'type_rating': subject['type_rating']})
                except GroupSubject.DoesNotExist:
                    newSubject = Subject(name=subject['subject'],
                                         subdepartament=Subdepartament.objects.get(code=subject['subDep']))
                    try:
                        newSubject.full_clean()
                        newSubject.save()
                    except ValidationError:
                        newSubject = Subject.objects.get(name=subject['subject'],
                                                         subdepartament=Subdepartament.objects.get(
                                                             code=subject['subDep']))
                    newGroupSubject = GroupSubject(subject=newSubject, group=group)
                    newGroupSubject.save()
                    listSubject.append({'subject': newGroupSubject,
                                        'type_rating': subject['type_rating']})
            students = group.students.all()
            for session in response['sessions']:
                for cell in session['session']:
                    record = Session(subject=listSubject[cell['numSubject']]['subject'],
                                     student=students.get(gradebook=session['gradeBook']),
                                     type_rating=listSubject[cell['numSubject']]['type_rating'],
                                     rating=cell['rating'])
                    try:
                        record.full_clean()
                        record.save()
                    except ValidationError:
                        record = Session.objects.get(subject=listSubject[cell['numSubject']]['subject'],
                                                     student=students.get(gradebook=session['gradeBook']),
                                                     type_rating=listSubject[cell['numSubject']]['type_rating'])
                        record.rating = cell['rating']
                        record.save()
            return True
        except Exception as err:
            return err

    def proveStudentInGroup(self, student, group, semester):
        gr = Group.objects.get(name=group, semester__id=semester)
        gr.students.add(student)
        gr.save()
