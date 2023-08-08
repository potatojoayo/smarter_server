from django.db import models

from business.models import Gym


class Level(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.PROTECT, related_name="levels")
    name = models.CharField(max_length=15)
    belt = models.CharField(max_length=20)
    belt_color = models.CharField(max_length=15, null=True)
    belt_brand = models.CharField(max_length=15, null=True)
    order = models.IntegerField()

    def __str__(self):
        return self.name
