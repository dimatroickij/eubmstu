from django.contrib import admin

# Register your models here.
from report.models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    # search_fields = ['name', 'code']
    # list_display = ('code', 'name')
    # list_per_page = 10
    pass
