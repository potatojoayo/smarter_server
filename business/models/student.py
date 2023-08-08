from django.db import models

from business.models import Gym


class Student(models.Model):
    name = models.CharField(max_length=10)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)


    def __str__(self):
        return self.name