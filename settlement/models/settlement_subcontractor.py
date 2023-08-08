from django.db import models

from settlement.models.settlement import Settlement
from business.models.subcontractor import Subcontractor


class SettlementSubcontractor(Settlement):
    subcontractor = models.ForeignKey(Subcontractor, on_delete=models.PROTECT)
    amount_sales = None
    amount_margin = None
    amount_platform_fee = None

    @property
    def amount_sales(self):
        raise AttributeError("'SettlementSubcontractor' object has no attribute 'amount_sames'")

    @property
    def amount_margin(self):
        raise AttributeError("'SettlementSubcontractor' object has no attribute 'amount_margin'")

    @property
    def amount_platform_fee(self):
        raise AttributeError("'SettlementSubcontractor' object has no attribute 'amount_platform_fee'")
