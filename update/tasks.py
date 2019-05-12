from control.getDataEU import getDataEU
from control.models import Semester, Departament, Subdepartament
from eubmstu.settings import USERNAME, PASSWORD


def updateSemester():
    eu = getDataEU(USERNAME, PASSWORD, False, True)
    try:
        eu.login()
        semesters = eu.getSemester()
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
        departaments = eu.getDep()
        for departament in departaments:
            try:
                find = Departament.objects.get(code=departament['code']).code
            except Departament.DoesNotExist:
                save = Departament(name=departament['name'], code=departament['code'],
                                   number=departament['number']).save()
        eu.exit()
        return True
    except Exception as err:
        eu.exit()
        return err


def updateSubdepartament():
    eu = getDataEU(USERNAME, PASSWORD, False, True)
    try:
        eu.login()
        departaments = Departament.objects.all()
        for dep in departaments:
            subDeps = eu.getSubDep(dep.number)
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