from django.db import models

from order.models import OrderDetail
from order.models.ta_order_master import TaOrderMaster


class TaOrderDetail(models.Model):
    ta_order_master = models.ForeignKey(TaOrderMaster, on_delete=models.CASCADE, related_name="ta_order_details")
    order_detail = models.ForeignKey(OrderDetail, on_delete=models.CASCADE, related_name="ta_order_details")
    price_special = models.IntegerField(null=True)
    total_price_special = models.IntegerField(null=True)
    is_deleted = models.BooleanField(default=False)
    class Meta:
        db_table = "ta_order_details"