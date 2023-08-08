from django.db import models

from gym_class.models import ClassMaster


class ClassDetail(models.Model):
    class_master = models.ForeignKey(ClassMaster, on_delete=models.CASCADE, related_name="class_details")
    day = models.IntegerField()
    hour_start = models.IntegerField()
    min_start = models.IntegerField()
    hour_end = models.IntegerField()
    min_end = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    date_deleted = models.DateTimeField(null=True)

    def __str__(self):
        return '{}, day:{} '.format(self.class_master, self.day)

