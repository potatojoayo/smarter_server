from django.db import models

from business.models import Gym
from gym_class.models import ClassMaster
from gym_class.models.class_detail import ClassDetail


class AttendanceMaster(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name="attendance_masters")
    class_master = models.ForeignKey(ClassMaster, on_delete=models.PROTECT, related_name="attendance_master")
    class_detail = models.ForeignKey(ClassDetail, on_delete=models.CASCADE, related_name="attendance_master")
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return '{} - {} - {} -{}'.format(self.gym, self.class_master, self.class_detail, self.date)
