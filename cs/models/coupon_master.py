from django.db import models


class CouponMaster(models.Model):
    price = models.IntegerField(null=True)
    count_per_issue = models.IntegerField(null=True) ## 유저당 발급되는 개수
    name = models.CharField(max_length=20, null=True) ## 쿠폰이름
    type = models.CharField(max_length=20, null=True) ## 쿠폰타입
    expire_day = models.IntegerField(null=True)
    coupon_message = models.CharField(max_length=100, null=True)
    is_deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'coupon_masters'

    @property
    def total_issued_count(self):
        return self.coupons.all().count()

    def __str__(self):
        return self.name