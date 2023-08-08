from django.db import models

from authentication.models import User
from cs.models import CsRequest


class ReturnRequest(models.Model):
    cs_request = models.ForeignKey(CsRequest, on_delete=models.CASCADE, related_name='returns', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='returns', null=True, blank=True)
    return_reason = models.CharField(max_length=100, null=True)
    receiver = models.CharField(max_length=15, null=True)
    phone = models.CharField(max_length=11, null=True)
    zip_code = models.CharField(blank=True, max_length=20, null=True)
    address = models.CharField(max_length=100, null=True)
    detail_address = models.CharField(max_length=100, null=True)
    total_products_price = models.IntegerField(null=True)
    delivery_price = models.IntegerField(null=True)
    is_delivery_price_exempt = models.BooleanField(null=True) ## True 시 스마터부담
    total_return_price = models.IntegerField(null=True)
    current_smarter_money = models.IntegerField(null=True)
    after_smarter_money = models.IntegerField(null=True)
    memo = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=10, default="반품요청")

    class Meta:
        db_table = 'return_requests'