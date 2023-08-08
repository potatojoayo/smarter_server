from django.db import models

from business.models.agency import Agency
from business.models.business import Business
from common.models import Membership


class Gym(Business):

    class Meta:
        ordering = ('-date_created',)

    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE, related_name='gym')
    owner_name = models.CharField(max_length=10, null=True, blank=True)
    manager_name = models.CharField(max_length=10, null=True, blank=True)
    agency = models.ForeignKey(Agency, on_delete=models.SET_NULL, null=True, related_name='gyms', blank=True)
    membership = models.ForeignKey(Membership, on_delete=models.PROTECT, related_name='membership', default=1)
    is_deduct_enabled = models.BooleanField(default=True)
    refund_bank_name = models.CharField(max_length=20, null=True)
    refund_bank_owner_name = models.CharField(max_length=30, null=True)
    refund_bank_account_no = models.CharField(max_length=50, null=True)
    class_payment_bank_name = models.CharField(max_length=20, null=True)
    class_payment_bank_owner_name = models.CharField(max_length=30, null=True)
    class_payment_bank_account_no = models.CharField(max_length=50, null=True)
    total_purchased_amount = models.IntegerField(default=0)
