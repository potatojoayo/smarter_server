from django.db import models

from order.models import EasyOrder


class EasyOrderFile(models.Model):

    class Meta:
        ordering = ('date_created', )

    easy_order = models.ForeignKey(EasyOrder, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='member/logo/request', null=True)
    date_created = models.DateTimeField(auto_now_add=True)
