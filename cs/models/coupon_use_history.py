from django.db import models

from business.models import Gym
from cs.models.coupon import Coupon
from order.models import OrderMaster


class CouponUseHistory(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.PROTECT, related_name='coupon_use_histories')
    order_master = models.ForeignKey(OrderMaster, on_delete=models.PROTECT, related_name='coupon_use_histories')
    gym = models.ForeignKey(Gym, on_delete=models.PROTECT, related_name='coupon_use_histories')
    coupon_number = models.CharField(max_length=20, null=True)
    order_number = models.CharField(max_length=25, unique=True)
    gym_name = models.CharField(max_length=50, null=True)
    price = models.IntegerField(null=True)
    date_used = models.DateTimeField(null=True)

    class Meta:
        db_table = 'coupon_use_histories'