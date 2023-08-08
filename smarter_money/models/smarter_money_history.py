from django.db import models

from order.models import OrderMaster
from smarter_money.models.wallet import Wallet


class SmarterMoneyHistory(models.Model):

    history_number = models.CharField(max_length=25)
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name='history')
    order_master = models.ForeignKey(OrderMaster, on_delete=models.CASCADE, related_name='smarter_money_history',
                                     null=True, blank=True)
    order_number = models.CharField(max_length=25, null=True, blank=True)
    transaction_type = models.CharField(max_length=10)  # '사용', '적립', '충전'
    description = models.CharField(max_length=100)
    amount = models.IntegerField()

    date_created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return '{} {} {}'.format(self.wallet.user.gym.name, self.date_created, self.amount)