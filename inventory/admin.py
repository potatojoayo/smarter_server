from django.contrib import admin

from inventory.models import InventoryReceivedDetail, InventoryReceivedMaster
from inventory.models.change_history import ChangeHistory
from inventory.models.inventory_order_master import InventoryOrderMaster
from inventory.models.inventory_order_detail import InventoryOrderDetail
from inventory.models.supplier import Supplier


@admin.register(ChangeHistory)
class ChangeHistoryAdmin(admin.ModelAdmin):
    pass


@admin.register(InventoryOrderMaster)
class InventoryOrderAdmin(admin.ModelAdmin):
    pass


@admin.register(InventoryReceivedMaster)
class InventoryReceivedMasterAdmin(admin.ModelAdmin):
    pass


@admin.register(InventoryReceivedDetail)
class InventoryReceivedDetailAdmin(admin.ModelAdmin):
    pass


@admin.register(InventoryOrderDetail)
class InventoryOrderedProductAdmin(admin.ModelAdmin):
    pass

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    pass
