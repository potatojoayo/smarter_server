from django.db import models


class Brand(models.Model):

    name = models.CharField(max_length=20)
    order = models.IntegerField()
    logo = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
