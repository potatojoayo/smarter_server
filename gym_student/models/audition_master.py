from django.db import models

from business.models import Gym
from gym_class.models.level import Level


class AuditionMaster(models.Model):
    current_level = models.ForeignKey(Level, on_delete=models.PROTECT, related_name="audition_masters_current")
    next_level = models.ForeignKey(Level, on_delete=models.PROTECT, related_name="audition_masters_next")
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name="audition_masters")
    date_audition = models.DateField()
    state = models.CharField(max_length=15, default="진행중")
    is_deleted = models.BooleanField(default=False)
    estimated_alarm_date = models.DateTimeField(null=True, blank=True)
