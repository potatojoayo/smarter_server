from django.db import models

from cs.models.return_request import ReturnRequest
from order.models import OrderDetail


class ReturnRequestDetail(models.Model):
    price_work = models.IntegerField(default=0)
    cs_request_return = models.ForeignKey(ReturnRequest, on_delete=models.CASCADE, related_name="return_details")
    order_detail = models.ForeignKey(OrderDetail, on_delete=models.PROTECT, related_name="return_details")
    return_quantity = models.IntegerField(null=True)
    return_price = models.IntegerField(null=True)
    class Meta:
        db_table = 'return_request_details'