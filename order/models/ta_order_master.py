from django.db import models

from business.models import TaFirm
from order.models import OrderMaster


class TaOrderMaster(models.Model):
    ta_firm = models.ForeignKey(TaFirm, on_delete=models.PROTECT, related_name="ta_order_masters")
    order_master = models.ForeignKey(OrderMaster, on_delete=models.CASCADE, related_name="ta_order_masters")
    order_number = models.CharField(max_length=25, null=True)
    gym_name = models.CharField(max_length=50, null=True)
    price_paid = models.IntegerField(default=0) ## 총 입금액
    price_delivery = models.IntegerField(default=0) ## 총 택배비
    price_to_be_paid = models.IntegerField() ## 입금요청금액
    is_paid = models.BooleanField(default=False)
    state = models.CharField(max_length=10, default='미결제')

    date_ordered = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "ta_order_masters"


    @property
    def total_price_special(self):
        details = self.ta_order_details.filter(is_deleted=False)
        price = 0
        for detail in details:
            price += detail.total_price_special
        return price