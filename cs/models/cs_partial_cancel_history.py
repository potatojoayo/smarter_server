from django.db import models

from cs.models.cs_request import CsRequest
from order.models import OrderDetail, OrderMaster


class CsPartialCancelHistory(models.Model):
    cs_request = models.ForeignKey(CsRequest, on_delete=models.CASCADE, related_name='cs_order_change_histories')
    order_master = models.ForeignKey(OrderMaster, on_delete=models.PROTECT, related_name='cs_order_change_histories')
    order_detail = models.ForeignKey(OrderDetail, on_delete=models.PROTECT, related_name='cs_order_change_histories')
    cs_request_number = models.CharField(max_length=15)
    order_number = models.CharField(max_length=20)
    product_name = models.CharField(max_length=100)
    gym_name = models.CharField(max_length=100)
    reason = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=20)
    size = models.CharField(max_length=20)
    price_product = models.IntegerField()
    price_total = models.IntegerField()
    canceled_quantity = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=30, null=True)
    class Meta:
        db_table = 'cs_partial_cancel_histories'
