from django.db import models

from business.models import Gym


class GymMonthlyPurchasedAmount(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='monthly_purchased_amount')
    date = models.DateField()
    amount = models.IntegerField(default=0)


