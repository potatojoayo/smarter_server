from django.db import models


class Banner(models.Model):

    class Meta:
        ordering = ('order',)

    image = models.ImageField()
    name = models.CharField(max_length=50)
    order = models.IntegerField()
