from psycopg2._psycopg import OperationalError

from control.getDataEU import getDataEU
from control.models import Semester, Departament, Subdepartament, Group, Student
from eubmstu.exceptions import EmptyListDeps, EmptyListSubDeps, EmptyListGroups, SubDepsNotFound
from eubmstu.settings import USERNAME, PASSWORD


def updateSemester():
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


def updateDepartament():
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


def updateSubdepartament():
    eu = getDataEU(USERNAME, PASSWORD, False, True)
    try:
        eu.login()
        departaments = Departament.objects.all().order_by('code')
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


def updateGroup(sems):
    eu = getDataEU(USERNAME, PASSWORD, False, True)
    try:
        eu.login()
        semesters = Semester.objects.filter(pk__in=sems)
        for semester in semesters:
            print(semester.name)
            try:
                subDeps = Subdepartament.objects.all()
                for subDep in subDeps:
                    try:
                        # print(subDep.code)
                        groups = eu.getGroups(subDep.departament.code, subDep.code, semester.code)
                        # print(groups)
                        for group in groups:
                            # pass
                            try:
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


def updateStudent(listDep):
    eu = getDataEU(USERNAME, PASSWORD, False, True)
    try:
        spisok = []
        eu.login()
        listLinkDeps = eu.getLinkDeps()
        for number in listDep:

            count = eu.getCountStudentsDep(listLinkDeps[number]['link'])
            print(listLinkDeps[number]['dep'] + ' ' + str(count))
            for num in range(1, count + 1):
                student = eu.getStudentDep(listLinkDeps[number]['link'], num)
                print(student)
                try:
                    find = Student.objects.get(gradebook=student['gradebook'])
                    z = find.gradebook
                    if find.last_name != student['name'].split(' ')[0]:
                        spisok.append(student)
                except Student.DoesNotExist:
                    name = student['name'].split(' ')
                    if len(name) == 2:
                        name.append('')
                    Student(last_name=name[0], first_name=name[1], patronymic=name[2],
                            gradebook=student['gradebook']).save()
        return spisok
    except Exception as err:
        return err
    finally:
        eu.exit()
