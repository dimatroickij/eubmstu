from control.getDataEU import getDataEU
from control.models import Semester
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
