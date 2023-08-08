from django.contrib import admin

from settlement.models.settlement_agency import SettlementAgency
from settlement.models.settlement_gym import SettlementGym
from settlement.models.settlement_state import SettlementState
from settlement.models.settlement_subcontractor import SettlementSubcontractor


@admin.register(SettlementAgency)
class SettlementAgencyAdmin(admin.ModelAdmin):
    pass


@admin.register(SettlementGym)
class SettlementGymAdmin(admin.ModelAdmin):
    pass


@admin.register(SettlementSubcontractor)
class SettlementSubcontractor(admin.ModelAdmin):
    pass


@admin.register(SettlementState)
class SettlementState(admin.ModelAdmin):
    pass
