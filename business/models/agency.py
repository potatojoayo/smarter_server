from django.db import models

from business.models.business import Business


class Agency(Business):
    class Meta:
        ordering = ('-date_created',)

    region = models.CharField(max_length=20 ,null=True, blank=True)
    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE, related_name='agency')




