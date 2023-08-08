from django.db import models

from inform.models.notification_type import NotificationType


class PushNotification(models.Model):

    to = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='push_notifications')
    title = models.CharField(max_length=100)
    contents = models.TextField()
    type = models.ForeignKey(NotificationType, on_delete=models.PROTECT, related_name='notifications')
    is_active = models.BooleanField(default=True)

    # DATE
    date_created = models.DateTimeField(auto_now_add=True)
