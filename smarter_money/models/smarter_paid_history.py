from django.db import models
from order.models import OrderDetail


class SmarterPaidHistory(models.Model):
    change_request = models.ForeignKey("cs.ChangeRequest", on_delete=models.PROTECT, related_name='smarter_paid_histories', blank=True, null=True)
    return_request = models.ForeignKey("cs.ReturnRequest", on_delete=models.PROTECT, related_name='smarter_paid_histories', blank=True, null=True)
    order_details = models.ManyToManyField(OrderDetail, related_name='smarter_paid_histories', blank=True)
    amount = models.IntegerField()
    reason = models.CharField(max_length=50)
