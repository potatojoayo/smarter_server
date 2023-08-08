from django.db import models

from business.models import Subcontractor


class SubcontractorCalculate(models.Model):
    class Meta:
        ordering = ('subcontractor', )

    subcontractor = models.ForeignKey(Subcontractor, on_delete=models.PROTECT, related_name='subcontractor_calculate')
    # 수량? 작업횟수?
    work_amount = models.IntegerField(default=0)
    # 작업비 총액
    total_price_work = models.IntegerField(default=0)
    # 정산금액(작업용역비 총액)
    total_price_work_labor = models.IntegerField(default=0)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    state = models.CharField(default="정산전", max_length=10)
    