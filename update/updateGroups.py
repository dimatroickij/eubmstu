from control.models import Semester
from update.tasks import UpdateData

ud = UpdateData()
semesters = range(1, len(Semester.objects.all()) + 1)
ud.updateGroups(semesters)
