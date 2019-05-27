from psycopg2._psycopg import OperationalError

from control.getDataEU import getDataEU
from control.models import Semester, Departament, Subdepartament, Group, Student, Subject
from eubmstu.exceptions import EmptyListDeps, EmptyListSubDeps, EmptyListGroups, SubDepsNotFound
from eubmstu.settings import USERNAME, PASSWORD

class updateData:

    def __init__(self):
        pass

    def updateSemester(self):
        eu = getDataEU(USERNAME, PASSWORD, False, True)
        try:
            eu.login()
            semesters = eu.getSemesters()
            for semester in semesters:
                try:
                    find = Semester.objects.get(name=semester['name']).name
                except Semester.DoesNotExist:
                    save = Semester(name=semester['name'], code=semester['link'], session=semester['session']).save()
            eu.exit()
            return True
        except Exception as err:
            eu.exit()
            return err


    def updateDepartament(self):
        eu = getDataEU(USERNAME, PASSWORD, False, True)
        try:

            eu.login()
            departaments = eu.getDepartaments()
            for departament in departaments:
                try:
                    find = Departament.objects.get(code=departament['code']).code
                except Departament.DoesNotExist:
                    save = Departament(name=departament['name'], code=departament['code'],
                                       number=departament['number']).save()
                print(departament)
            eu.exit()
            return True
        except Exception as err:
            eu.exit()
            return err


    def updateSubdepartament(self):
        eu = getDataEU(USERNAME, PASSWORD, False, True)
        try:
            eu.login()
            departaments = Departament.objects.exclude(code='АДМИН').order_by('code')
            for dep in departaments:
                subDeps = eu.getSubDepartaments(dep.code)
                for subDep in subDeps:
                    try:
                        find = Subdepartament.objects.get(code=subDep['code']).code
                    except Subdepartament.DoesNotExist:
                        save = Subdepartament(name=subDep['name'], code=subDep['code'],
                                              number=subDep['number'], departament=dep).save()
            eu.exit()
            return True
        except Exception as err:
            eu.exit()
            return err


    def updateGroup(self, sems):
        eu = getDataEU(USERNAME, PASSWORD, False, True)
        try:
            eu.login()
            semesters = Semester.objects.filter(pk__in=sems)
            for semester in semesters:
                print(semester.name)
                try:
                    subDeps = Subdepartament.objects.exclude(departament__code='АДМИН')
                    for subDep in subDeps:
                        try:
                            # print(subDep.code)
                            groups = eu.getGroups(subDep.departament.code, subDep.code, semester.code)
                            # print(groups)
                            for group in groups:
                                # pass
                                try:
                                    if group['isEmpty'] == '':
                                        isEmpty = False
                                    else:
                                        isEmpty = True
                                    find = Group.objects.get(code=group['code'], semester=semester, name=group['name']).code
                                except Group.DoesNotExist:
                                    if group['isEmpty'] == '':
                                        isEmpty = False
                                    else:
                                        isEmpty = True
                                    Group(name=group['name'], code=group['code'], semester=semester, subdepartament=subDep,
                                          levelEducation=group['levelEducation'], isEmpty=isEmpty).save()
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
        finally:
            eu.exit()


    def updateStudent(self, listDep):
        eu = getDataEU(USERNAME, PASSWORD, False, True)
        try:
            eu.login()
            listLinkDeps = eu.getLinkDeps()
            for number in listDep:

                count = eu.getCountStudentsDep(listLinkDeps[number]['link'])
                print(listLinkDeps[number]['dep'] + ' ' + str(count))
                for num in range(1, count + 1):
                    print(str(num) + '/' + str(count))
                    student = eu.getStudentDep(listLinkDeps[number]['link'], num)
                    # print(student)
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
        finally:
            eu.exit()


    def updateSubjectsInGroup(self, group, session):
        eu = getDataEU(USERNAME, PASSWORD, False, True)
        try:
            eu.login()
            listSubjects = eu.getProgressInGroup(group, session, True, False, False)
            for subject in listSubjects['subjects']:
                try:
                    find = Subject.objects.get(name=subject['subject'], subdepartament=Subdepartament.objects.get(code=subject['subDep'])).name
                except Subject.DoesNotExist:
                    Subject(name=subject['subject'], subdepartament=Subdepartament.objects.get(code=subject['subDep'])).save()
            return True
        except Exception as err:
            return err
        finally:
            eu.exit()


    def updateStudentsInGroup(self, code, semester):
        group = Group.objects.get(code=code, semester__code=semester)
        eu = getDataEU(USERNAME, PASSWORD, False, True)
        try:
            eu.login()
            listStudents = eu.getProgressInGroup(code, semester, False, True, False)

            for student in listStudents['students']:
                find = Student.objects.get(last_name=student['student'], gradebook=student['gradeBook'])
                z = find.last_name
                if Group.objects.filter(students=find, semester__code=semester).exclude(pk=group.pk).count() != 0:
                    lastGroup = Group.objects.get(students=find, semester__code=semester)
                    lastGroup.students.remove(find)
                group.students.add(find)
            return True
        except Exception as err:
            return err
        finally:
            eu.exit()

    def updateProgressInGroup(self, code, semester, student):
        group = Group.objects.get(code=code, semester__code=semester)
        eu = getDataEU(USERNAME, PASSWORD, False, True)
        try:
            eu.login()
            listProgress = eu.getProgressInGroup(code, semester, False, False, True)
            for progress in listProgress['progress']:
                find = Student.objects.get(last_name=student['student'], gradebook=student['gradeBook'])
                z = find.last_name
                if Group.objects.filter(students=find, semester__code=semester).exclude(pk=group.pk).count() != 0:
                    lastGroup = Group.objects.get(students=find, semester__code=semester)
                    lastGroup.students.remove(find)
                group.students.add(find)
            return True
        except Exception as err:
            return err
        finally:
            eu.exit()


    def proveStudentInGroup(self, student, group, semester):
        gr = Group.objects.get(name=group, semester__id=semester)
        gr.students.add(student)
        gr.save()
