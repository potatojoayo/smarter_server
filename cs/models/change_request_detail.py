from django.db import models

from cs.models.change_request import ChangeRequest
from order.models import Delivery, OrderDetail
from product.models import Product


class ChangeRequestDetail(models.Model):
    cs_request_change = models.ForeignKey(ChangeRequest, on_delete=models.CASCADE, related_name="change_details")
    changed_product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='changed_products', null=True)
    price_work = models.IntegerField(default=0)
    changing_product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='changing_products', null=True)
    changing_quantity = models.IntegerField(null=True)
    total_changing_price = models.IntegerField(null=True)
    changing_price = models.IntegerField(default=0)
    order_detail = models.ForeignKey(OrderDetail, on_delete=models.PROTECT, related_name='change_details', null=True)
    class Meta:
        db_table = 'change_request_details'