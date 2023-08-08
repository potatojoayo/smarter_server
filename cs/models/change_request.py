from django.db import models

from authentication.models import User
from cs.models import CsRequest
from order.models import Delivery


class ChangeRequest(models.Model):
    cs_request = models.ForeignKey(CsRequest, on_delete=models.CASCADE, related_name="changes", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='changes', null=True, blank=True)
    delivery = models.OneToOneField(Delivery, on_delete=models.PROTECT, related_name="change", null=True)
    change_reason = models.CharField(max_length=100, null=True)
    pick_up_receiver = models.CharField(max_length=15, null=True)
    pick_up_phone = models.CharField(max_length=11, null=True)
    pick_up_address = models.CharField(max_length=100, null=True)
    pick_up_detail_address = models.CharField(max_length=100, null=True)
    pick_up_zip_code = models.CharField(max_length=5, null=True, blank=True)
    delivery_receiver = models.CharField(max_length=15, null=True)
    delivery_phone = models.CharField(max_length=11, null=True)
    delivery_address = models.CharField(max_length=100, null=True)
    delivery_detail_address = models.CharField(max_length=100, null=True)
    delivery_zip_code = models.CharField(max_length=5, null=True, blank=True)
    total_changing_price = models.IntegerField(null=True)
    is_changed_price_exempt = models.BooleanField(default=False)
    delivery_price = models.IntegerField(default=0)
    is_delivery_price_exempt = models.BooleanField(default=False)
    payment_amount = models.IntegerField(null=True)
    current_smarter_money = models.IntegerField(null=True)
    after_smarter_money = models.IntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=10, default="교환요청")
    memo = models.TextField(null=True)
    price_to_pay = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'change_requests'