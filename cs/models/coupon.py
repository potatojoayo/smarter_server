from django.db import models

from authentication.models import User
from business.models import Gym
from cs.models.coupon_issue_history import CouponIssueHistory


class Coupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='coupons')
    coupon_master = models.ForeignKey('cs.CouponMaster', on_delete=models.PROTECT, related_name='coupons')
    coupon_number = models.CharField(max_length=20, null=True, unique=True)
    price = models.IntegerField(null=True)
    date_used = models.DateTimeField(null=True, blank=True)
    start_of_use = models.DateTimeField(null=True)
    end_of_use = models.DateTimeField(null=True)
    date_issued = models.DateTimeField(auto_now_add=True, null=True)

    #추천인 코드
    referral_code = models.CharField(max_length=11, null=True, blank=True)

    # 피추천인
    nominee = models.ForeignKey(Gym, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'coupons'

    def save(self, *args, **kwargs):
        created = False
        if not self.pk:
            created = True
        super(Coupon, self).save(*args, **kwargs)
        if created:
            CouponIssueHistory.objects.create(coupon=self, gym=self.user.gym, coupon_number=self.coupon_number,
                                              gym_name=self.user.gym.name, price=self.price, start_of_use=self.start_of_use, end_of_use=self.end_of_use)