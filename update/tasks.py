from control.getDataEU import getDataEU
from control.models import Semester, Departament
from eubmstu.settings import USERNAME, PASSWORD


def updateSemester():
    try:
        eu = getDataEU(USERNAME, PASSWORD, False, True)
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
        return err


def updateDepartament():
    try:
        eu = getDataEU(USERNAME, PASSWORD, False, True)
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
        return err
