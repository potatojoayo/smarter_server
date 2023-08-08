from django.db import models

from business.models import Gym


class CouponIssueHistory(models.Model):
    coupon = models.ForeignKey('cs.Coupon', on_delete=models.PROTECT, related_name='coupon_issue_histories')
    gym = models.ForeignKey(Gym, on_delete=models.PROTECT, related_name='coupon_issue_histories')
    coupon_number = models.CharField(max_length=20, null=True)
    gym_name = models.CharField(max_length=50)
    price = models.IntegerField(null=True)
    date_issued = models.DateTimeField(auto_now_add=True)
    start_of_use = models.DateTimeField(null=True)
    end_of_use = models.DateTimeField(null=True)


    class Meta:
        db_table = 'coupon_issue_histories'
