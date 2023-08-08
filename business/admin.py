from django.contrib import admin

from business.models import TaFirm
from business.models.agency import Agency
from business.models.gym import Gym
from business.models.subcontractor import Subcontractor
from business.models.vendor import Vendor


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    pass

@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    search_fields = ('user__id', 'name')
    list_display = ('id','name', 'membership', 'user')

@admin.register(Subcontractor)
class SubcontractorAdmin(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    pass


@admin.register(TaFirm)
class TaFirmAdmin(admin.ModelAdmin):
    pass
