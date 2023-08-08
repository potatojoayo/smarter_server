from django.db import models


class SettlementState(models.Model):

    name = models.CharField(max_length=10)

