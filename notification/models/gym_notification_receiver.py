from django.db import models

from gym_student.models import Parent
from notification.models.gym_notification import GymNotification


class GymNotificationReceiver(models.Model):
    gym_notification = models.ForeignKey(GymNotification, on_delete=models.CASCADE, related_name="receivers")
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name="notification_receivers")
    date_read = models.DateTimeField(null=True, blank=True)
