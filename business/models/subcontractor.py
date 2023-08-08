from django.utils import timezone
from django.db import models

from business.models.business import Business


class Subcontractor(Business):

    class Meta:
        ordering = ('id',)

    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE, related_name='subcontractor', null=True, blank=True)
    is_out_working = models.BooleanField(default=False)
    is_pre_working = models.BooleanField(default=False)

    @property
    def daily_cumulative_work(self):
        # today = timezone.localtime()
        return self.works.filter(state='작업중').count()



