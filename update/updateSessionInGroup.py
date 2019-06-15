from control.models import Group, Semester
from update.tasks import UpdateData

ud = UpdateData()
semester = Semester.objects.order_by('pk')[23]
groups = Group.objects.filter(subdepartament__code='ИУ6', semester=semester)
isMain = True
for group in groups:
    print('start %s' % group.name)
    ud.updateSessionInGroup(group.code, semester.code, isMain)
    if isMain:
        isMain = False