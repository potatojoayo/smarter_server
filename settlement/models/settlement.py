from django.db import models

from settlement.models.settlement_state import SettlementState


class Settlement(models.Model):

    state = models.ForeignKey(SettlementState, on_delete=models.PROTECT)

    # AMOUNT
    amount_sales = models.IntegerField()
    amount_margin = models.IntegerField()
    amount_platform_fee = models.IntegerField()
    amount_settled = models.IntegerField()

    # DATE
    date_created = models.DateTimeField(auto_now_add=True)
    date_from = models.DateTimeField(null=True)
    date_to = models.DateTimeField(null=True)

    class Meta:
        abstract = True
