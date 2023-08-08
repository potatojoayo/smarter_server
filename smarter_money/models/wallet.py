from django.db import models


class Wallet(models.Model):

    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE, related_name='wallet')
    balance = models.IntegerField(default=0)