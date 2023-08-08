from django.contrib import admin

from order.models import EasyOrder, Payment, ZipCode, Delivery, WorkDetail, EasyOrderImage, EasyOrderFile, \
    TaOrderMaster, TaOrderDetail
from order.models.claim import Claim
from order.models.order_detail import OrderDetail
from order.models.order_master import OrderMaster
from order.models.work import Work


@admin.register(EasyOrderFile)
class EasyOrderFile(admin.ModelAdmin):
    pass


@admin.register(EasyOrderImage)
class EasyOrderImage(admin.ModelAdmin):
    pass


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderMaster)
class OrderMasterAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_number','date_created', 'price_delivery')
    search_fields = ('order_number', )


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('id','state', 'product', 'quantity', 'price_total', 'order_master','draft')
    search_fields = ('order_master__order_number', )


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('id','subcontractor', 'date_created')


@admin.register(EasyOrder)
class EasyOrderAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'state', 'date_updated', 'date_created')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass

@admin.register(ZipCode)
class ZipCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'address','additional_delivery_price')
    search_fields = ('address',)

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    pass


@admin.register(WorkDetail)
class WorkDetailAdmin(admin.ModelAdmin):
    pass

@admin.register(TaOrderMaster)
class TaOrderMasterAdmin(admin.ModelAdmin):
    list_display = ('id', "ta_firm", 'gym_name', 'order_number')
    save_as = True

@admin.register(TaOrderDetail)
class TaOrderDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'ta_order_master')
    save_as = True
