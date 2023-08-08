from django.db import models

from business.models import Gym
from common.models import AddressZipCode
from cs.models import CouponMaster


class CouponMasterIssueHistory(models.Model):

    coupon_master = models.ForeignKey(CouponMaster, on_delete=models.PROTECT,)
    issued_gyms = models.ManyToManyField(Gym)
    issued_address = models.ForeignKey(AddressZipCode, on_delete=models.PROTECT, null=True, blank=True)
    condition = models.CharField(max_length=10, null=True, blank=True)
    threshold_amount = models.IntegerField(null=True, blank=True)
    issued_count_per_gym = models.IntegerField()
    issued_amount_per_gym = models.IntegerField()
    search_type = models.CharField(max_length=10)
    total_issued_count = models.IntegerField()
    total_issued_amount = models.IntegerField()
    expired_day = models.IntegerField()
    coupon_message = models.TextField()
    date_issued = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'manual_coupon_master_issue_histories'
