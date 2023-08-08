from django.db import models


class Category(models.Model):

    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children',default=None)
    order = models.IntegerField(default=-1)
    depth = models.IntegerField(default=0)

    def __str__(self):
        return self.name


