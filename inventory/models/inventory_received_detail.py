from django.db import models

from inventory.models import InventoryOrderDetail
from inventory.models.inventory_received_master import InventoryReceivedMaster


class InventoryReceivedDetail(models.Model):
    class Meta:
        ordering = ('id',)
    inventory_order_detail = models.ForeignKey(InventoryOrderDetail, on_delete=models.PROTECT, related_name='inventory_received')
    inventory_received_master = models.ForeignKey(InventoryReceivedMaster, on_delete=models.CASCADE, related_name='details')
    name = models.CharField(max_length=20, null=True)
    color = models.CharField(max_length=10, null=True)
    size = models.CharField(max_length=10, null=True)

    #단가
    price_vendor = models.IntegerField(null=True)
    #발주수량
    quantity_ordered = models.IntegerField(null=True)
    #발주금액
    price_ordered = models.IntegerField(null=True)
    #입고수량
    quantity_received = models.IntegerField(null=True, blank=True)
    #미입고수량
    quantity_not_received = models.IntegerField(null=True,blank=True)
    #입고금액
    price_received = models.IntegerField(null=True)
    #미입고사유
    reason_not_received = models.CharField(max_length=50, null=True)
    # 추가입고수량
    quantity_additional_received = models.IntegerField(null=True)
    # 추가입고금액
    price_additional_received = models.IntegerField(null=True)
