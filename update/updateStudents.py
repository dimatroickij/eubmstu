from control.models import Departament
from update.tasks import UpdateData

ud = UpdateData()
deps = range(0, len(Departament.objects.all()))
ud.updateStudents(deps)
