from django.db import models


class Membership(models.Model):

    class Meta:
        ordering = ('id',)

    name = models.CharField(max_length=20)
    condition = models.IntegerField(null=True)
    threshold = models.IntegerField(null=True)
    percentage = models.FloatField(null=True)
    max = models.IntegerField(null=True)

    def __str__(self):
        return self.name
