from django.db import models

from product.models import ProductMaster, Draft


class DraftRequest(models.Model):
    class Meta:
        ordering = ['-date_created']

    user = models.ForeignKey('authentication.User', on_delete=models.PROTECT, related_name='draft_requests')
    state = models.CharField(max_length=10)

    date_created = models.DateTimeField(auto_now_add=True)
    date_finished = models.DateTimeField(null=True, blank=True)
