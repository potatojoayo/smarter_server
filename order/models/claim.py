from django.db import models

from order.models import OrderDetail


class Claim(models.Model):

    class Meta:
        ordering = (
            '-date_created',
        )

    order_detail = models.ForeignKey(OrderDetail, on_delete=models.CASCADE, related_name='claims')
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='claims')

    quantity = models.IntegerField()
    price_total = models.IntegerField()
    price_products = models.IntegerField()
    price_total_work = models.IntegerField()
    price_total_work_labor = models.IntegerField()

    state = models.CharField(max_length=10) # 교환요청, 교환완료, 반품요청, 반품완료, 교환반려, 반품반려
    reason = models.CharField(max_length=255)

    refund_price = models.IntegerField(null=True)

    # Date
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

