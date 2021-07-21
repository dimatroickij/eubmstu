import re

from django.core.exceptions import ValidationError, MultipleObjectsReturned
from psycopg2 import OperationalError

from control.GetDataEU import GetDataEU
from control.models import Semester, Departament, Subdepartament, Group, Student, Subject, GroupSubject, Progress, \
    Session
from eubmstu.exceptions import SubDepsNotFound, EmptyListSubDeps, EmptyListDeps
from eubmstu.settings import USERNAME, PASSWORD


class UpdateData:

    def __init__(self):
        self.eu = GetDataEU(USERNAME, PASSWORD)
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
            departaments = Departament.objects.exclude(code='АДМИН').exclude(code='ФВ').order_by('code')
            for dep in departaments:
                subDeps = self.eu.getSubDepartaments(dep.code)
                print('Факультет %s, количество кафедр: %i' % (dep.code, len(subDeps)))
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

    # 8.47 минут - обновление весеннего семестра 2018-2019
    def updateGroups(self, sems):
        try:
            semesters = Semester.objects.filter(pk__in=sems)
            for semester in semesters:
                # print(semester.name)
                try:
                    subDeps = Subdepartament.objects.exclude(departament__code='АДМИН').exclude(
                        departament__code='ФВ').exclude(code__contains='АДМИН')
                    for subDep in subDeps:
                        try:
                            groups = self.eu.getGroups(subDep.code, semester.code)
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

    def updateStudents(self):
        try:
            listLinkDeps = self.eu.getLinkDeps()
            for linkDeps in listLinkDeps:

                count = self.eu.getCountStudentsDep(linkDeps['link'])
                print(linkDeps['dep'] + ' ' + str(count))
                students = self.eu.getStudents(linkDeps['link'])
                try:
                    self.saveStudents(students)
                except OperationalError:
                    self.saveStudents(students)
        except Exception as err:
            return err

    def saveStudents(self, students):
        for student in students:
            name = student['student'].split(' ')
            if len(name) == 2:
                name.append('')
            try:
                stud = Student(last_name=name[0], first_name=name[1], patronymic=name[2],
                               gradebook=student['gradeBook'], uuid=student['uuid'])
                try:
                    stud.full_clean()
                    stud.save()
                except ValidationError:
                    pass
            except OperationalError:
                self.saveStudents(student)

    # def updateSubjectsInGroup(self, groupCode, semester):
    #     group = Group.objects.get(code=groupCode, semester__code=semester)
    #     try:
    #         listSubjects = self.eu.getProgressInGroup(groupCode, semester, True, False, False)
    #         for subject in listSubjects['subjects']:
    #             try:
    #                 subDep = Subdepartament.objects.get(code=subject['subDep'])
    #             except Subdepartament.DoesNotExist:
    #                 try:
    #                     subDep = Subdepartament(code=subject['subDep'], name=subject['subDep'],
    #                                             departament=Departament.objects.get(
    #                                                 code=re.sub(r'\d+', '', subject['subDep'])))
    #                 except Departament.DoesNotExist:
    #                     dep = Departament(code=re.sub(r'\d+', '', subject['subDep']),
    #                                       name=re.sub(r'\d+', '', subject['subDep']))
    #                     dep.save()
    #                     subDep = Subdepartament(code=subject['subDep'], name=subject['subDep'], departament=dep)
    #                 subDep.full_clean()
    #                 subDep.save()
    #                 recordSubject = Subject(name=subject['subject'], subdepartament=subDep)
    #                 recordSubject.save()
    #             try:
    #                 recordSubject = Subject.objects.get(name=subject['subject'], subdepartament=subDep)
    #             except Subject.DoesNotExist:
    #                 recordSubject = Subject(name=subject['subject'], subdepartament=subDep)
    #                 recordSubject.save()
    #             try:
    #                 record = GroupSubject(group=group, subject=recordSubject)
    #                 record.full_clean()
    #                 record.save()
    #             except ValidationError:
    #                 pass
    #         return True
    #     except RuntimeError as err:
    #         return err

    # def updateStudentsInGroup(self, code, semester):
    #     group = Group.objects.get(code=code, semester__code=semester)
    #     try:
    #         # oldStudents = list(group.students.all().values('gradeBook', 'last_name'))
    #         newListStudents = self.eu.getProgressInGroup(code, semester, False, True, False)
    # 
    #         for i, student in enumerate(newListStudents['students']):
    #             try:
    #                 find = Student.objects.get(last_name=student['student'].split(' ')[0],
    #                                            gradebook=student['gradeBook'])
    #                 if find.uuid is None or find.uuid == '':
    #                     find.uuid = student['uuid']
    #                     find.save()
    #             except Student.DoesNotExist:
    #                 try:
    #                     find = Student.objects.get(pk=self.saveStudents([student]))
    #                 except Student.DoesNotExist:
    #                     find = Student.objects.get(gradebook='000000')
    #                 # try:
    #                 #     oldStudents.remove({'gradeBook': student['gradeBook']})
    #                 # except ValueError:
    #                 #     pass
    #                 # if len(oldStudents) != 0:
    #                 #     for old in oldStudents:
    #                 #         group.students.remove(Student.objects.get(gradebook=old['gradeBook']))
    #             if Group.objects.filter(students=find, semester__code=semester).exclude(pk=group.pk).count() != 0:
    #                 lastGroup = Group.objects.get(students=find, semester__code=semester)
    #                 lastGroup.students.remove(find)
    #             group.students.add(find)
    #         return True
    #     except RuntimeError as err:
    #         return err

    def updateSubjectsInGroup(self, listSubjects, group):
        subjects = []
        for subject in listSubjects:
            try:
                subjects.append(GroupSubject.objects.get(group=group, subject__name=subject['subject'],
                                                         subject__subdepartament__code=subject['subDep']))
            except GroupSubject.DoesNotExist:
                try:
                    newSubject = Subject.objects.get(name=subject['subject'], subdepartament__code=subject['subDep'])
                    sub = newSubject.name
                except Subject.DoesNotExist:
                    newSubject = Subject(name=subject['subject'],
                                         subdepartament=Subdepartament.objects.get(code=subject['subDep']))
                    newSubject.full_clean()
                    newSubject.save()
                newGroupSubject = GroupSubject(subject=newSubject, group=group)
                newGroupSubject.save()
                subjects.append(newGroupSubject)
        return subjects

    def updateStudentsInGroup(self, lastStudents, group):
        newListStudents = []
        students = group.students.all()
        for student in lastStudents:
            try:
                find = students.get(gradebook=student['gradeBook'],
                                    last_name=student['student'].split(' ')[0])
                if find.uuid == '' or find.uuid is None:
                    find.uuid = student['uuid']
                    find.save()
            except Student.DoesNotExist:
                try:
                    find = Student.objects.get(gradebook=student['gradeBook'],
                                               last_name=student['student'].split(' ')[0])
                    if find.uuid == '' or find.uuid is None:
                        find.uuid = student['uuid']
                        find.save()
                except Student.DoesNotExist:
                    name = student['student'].strip().split(' ')
                    if len(name) == 2:
                        name.append('')
                    find = Student(last_name=name[0], first_name=name[1], patronymic=name[2],
                                   gradebook=student['gradeBook'], uuid=student['uuid'])
                    find.full_clean()
                    find.save()
                group.students.add(find)
            newListStudents.append(find)
        return newListStudents

    def updateProgressInGroup(self, code, semester):
        group = Group.objects.get(code=code, semester__code=semester)
        try:
            listProgress = self.eu.getProgressInGroup(code, semester, True, True, True)
            subjects = self.updateSubjectsInGroup(listProgress['subjects'], group)
            students = self.updateStudentsInGroup(listProgress['students'], group)
            for i, student in enumerate(students):
                for j, subject in enumerate(subjects):
                    try:
                        record = Progress(subject=subject, student=student,
                                          point=listProgress['progress'][i][j]['point'])
                        record.full_clean()
                        record.save()
                    except ValidationError:
                        record = Progress.objects.get(subject=subject, student=student)
                        record.point = listProgress['progress'][i][j]['point']
                        record.save()
            return True
        except RuntimeError as err:
            return err

    def updateSessionInGroup(self, code, semester, isMain=False):
        group = Group.objects.get(code=code, semester__code=semester)
        try:
            response = self.eu.getSessionInGroup(code, semester, isMain)
            if response:
                subjects = self.updateSubjectsInGroup(response['subjects'], group)
                students = self.updateStudentsInGroup(response['students'], group)
                for i, student in enumerate(students):
                    for j, subject in enumerate(subjects):
                        try:
                            record = Session(subject=subject, student=student,
                                             type_rating=response['sessions'][i][j]['type_rating'],
                                             rating=response['sessions'][i][j]['rating'])
                            record.full_clean()
                            record.save()
                        except ValidationError:
                            record = Session.objects.get(subject=subject, student=student,
                                                         type_rating=response['sessions'][i][j]['type_rating'])
                            record.rating = response['sessions'][i][j]['rating']
                            record.save()
            return True
        except RuntimeError as err:
            return err
