from django.db import models

from notification.models.gym_notification import GymNotification


class GymNotificationImages(models.Model):
    gym_notification = models.ForeignKey(GymNotification, on_delete=models.CASCADE,
                                         related_name='images')
    image = models.ImageField(default=None)
