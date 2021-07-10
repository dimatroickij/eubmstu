from control.models import Group
from update.tasks import UpdateData


class updateDB:

    def __init__(self):
        self.s = UpdateData()

    def updateSemesters(self):
        print('Обновление семестров')
        self.s.updateSemesters()

    def updateDepartaments(self):
        print('Обновление факультетов')
        self.s.updateDepartaments()

    def updateSubDepartaments(self):
        print('Обновление кафедр')
        self.s.updateSubDepartaments()

    def updateGroups(self, semester=None):
        print('Обновление групп семестра %s' % semester)
        self.s.updateGroups(semester)

    def updateStudents(self):
        print('Обновление БД студентов')
        self.s.updateStudents()

    def updateSubjectsInGroup(self, group, semester):
        print('Обновление предметов в группе %s' % group)
        self.s.updateSubjectsInGroup(group, semester)

    def updateSubjectsInSemester(self, semester, start=0):
        print('Обновление предметов в группах семестра %s' % semester)
        groups = Group.objects.filter(semester__code=semester)[start:]
        count = len(groups)
        i = 1
        for group in groups:
            print('%i / %i Группа %s' % (i, count, group.name))
            i += 1
            self.s.updateSubjectsInGroup(group.code, semester)

    def updateStudentsInGroup(self, group, semester):
        print('Обновление студентов в группе %s' % group)
        self.s.updateStudentsInGroup(group, semester)

    def updateStudentsInSemester(self, semester, start=0):
        print('Обновление студентов в группах семестра %s' % semester)
        groups = Group.objects.filter(semester__code=semester)[start:]
        count = len(groups)
        i = 1
        for group in groups:
            print('%i / %i Группа %s' % (i, count, group.name))
            i += 1
            self.s.updateStudentsInGroup(group.code, semester)

    def updateProgressInGroup(self, group, semester):
        print('Обновление успеваемости в группе %s семестра %s' % (group, semester))
        self.s.updateProgressInGroup(group, semester)

    def updateProgressInSemester(self, semester, start=0):
        print('Обновление успеваемости в группах семестра %s' % semester)
        groups = Group.objects.filter(semester__code=semester)[start:]
        count = len(groups)
        i = 1
        for group in groups:
            print('%i / %i Группа %s' % (i, count, group.name))
            i += 1
            self.s.updateProgressInGroup(group.code, semester)

    def updateSubAndStudAndProgressInGroup(self, group, semester):
        print('Обновление предметов, списка студентов, успеваемости в группе %s семестра %s' % (group, semester))
        self.s.updateSubjectsInGroup(group, semester)
        self.s.updateStudentsInGroup(group, semester)
        self.s.updateProgressInGroup(group, semester)

    def updateSubAndStudAndProgressInSemester(self, semester, start=0):
        print('Обновление предметов, списка студентов, успеваемости в группах семестра %s' % semester)
        groups = Group.objects.filter(semester__code=semester)[start:]
        count = len(groups)
        i = 1
        for group in groups:
            print('%i / %i Группа %s' % (i, count, group.name))
            i += 1
            self.s.updateSubjectsInGroup(group.code, semester)
            self.s.updateStudentsInGroup(group.code, semester)
            self.s.updateProgressInGroup(group.code, semester)

    def updateSubAndStudInGroup(self, group, semester):
        print('Обновление предметов, списка студентов, успеваемости в группе %s семестра %s' % (group, semester))
        self.s.updateSubjectsInGroup(group, semester)
        self.s.updateStudentsInGroup(group, semester)

    def updateSubAndStudInSemester(self, semester, start=0):
        print('Обновление предметов, списка студентов в группах семестра %s' % semester)
        groups = Group.objects.filter(semester__code=semester)[start:]
        count = len(groups)
        i = 1
        for group in groups:
            print('%i / %i Группа %s' % (i, count, group.name))
            i += 1
            self.s.updateSubjectsInGroup(group.code, semester)
            self.s.updateStudentsInGroup(group.code, semester)

    def updateSessionInGroup(self, group, semester, isMain=False):
        print('Обновление результатов сессии в группе %s семестра %s' % (group, semester))
        self.s.updateSessionInGroup(group, semester, isMain)

    def updateSessionInSemester(self, semester, start=0, isMain=False):
        print('Обновление результатов сессии в группах семестра %s' % semester)
        groups = Group.objects.filter(semester__code=semester)[start:]
        count = len(groups)
        i = 1
        f = open('%s.txt' % semester, 'a')
        for group in groups:
            print('%i / %i Группа %s' % (i, count, group.name))
            f.write('%i / %i Группа %s\n' % (i, count, group.name))
            i += 1
            self.s.updateSessionInGroup(group.code, semester, isMain)
        f.close()
