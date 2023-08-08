from django.db import models

from cs.models import CsRequest
from order.models import OrderMaster


class CancelOrderRequest(models.Model):

    cs_request = models.ForeignKey(CsRequest, on_delete=models.PROTECT, null=True, blank=True)
    cs_request_number = models.CharField(max_length=20, null=True, blank=True)
    order_master = models.ForeignKey(OrderMaster, on_delete=models.PROTECT)
    order_number = models.CharField(max_length=25)
    gym_name = models.CharField(max_length=20)
    reason = models.CharField(max_length=100, null=True, blank=True)
    price_products = models.IntegerField()
    price_works = models.IntegerField()
    price_delivery = models.IntegerField()
    price_total = models.IntegerField()
    state = models.CharField(max_length=10)
    date_created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    is_without_deposit = models.BooleanField(default=False)

    class Meta:
        db_table = 'cancel_order_requests'
