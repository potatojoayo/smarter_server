from django.db import models

from business.models import Agency


class AgencyCalculate(models.Model):
    class Meta:
        ordering = ('agency', )

    agency = models.ForeignKey(Agency, on_delete=models.PROTECT, related_name='agency_calculate')
    #소속 체육관 매출 합계
    agency_total_sell = models.IntegerField(default=0)
    #정산 대상 금액
    price_profit = models.IntegerField(default=0)
    #스마터플랫폼 사용로
    price_platform = models.IntegerField(default=0)

    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    state = models.CharField(default="정산전", max_length=10)

    @property
    def net_profit(self):
        return self.price_profit - self.price_platform

