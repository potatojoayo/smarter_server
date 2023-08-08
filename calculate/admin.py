from django.contrib import admin

from calculate.models.agency_calculate import AgencyCalculate
from calculate.models.subcontractor_calculate import SubcontractorCalculate


# Register your models here.
@admin.register(AgencyCalculate)
class AgencyCalculateAdmin(admin.ModelAdmin):
    pass

@admin.register(SubcontractorCalculate)
class SubcontractorCalculateAdmin(admin.ModelAdmin):
    list_display = ('subcontractor', 'total_price_work','total_price_work_labor')