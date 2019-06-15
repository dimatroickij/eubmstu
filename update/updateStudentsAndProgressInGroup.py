from control.models import Group, Semester
from update.tasks import UpdateData

ud = UpdateData()
semester = Semester.objects.order_by('pk')[23]
groups = Group.objects.filter(subdepartament__code='ИУ6', semester=semester)
for group in groups:
    print('updateSubjects')
    ud.updateSubjectsInGroup(group.code, semester.code)
    print('updateStudents')
    ud.updateStudentsInGroup(group.code, semester.code)
    print('updateProgress')
    ud.updateProgressInGroup(group.code, semester.code)
    print('end %s' % group.name)