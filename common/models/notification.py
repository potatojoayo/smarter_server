from django.db import models


class Notification(models.Model):

    class Meta:
        ordering = ('-date_created',)

    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=30)
    contents = models.TextField()
    notification_type = models.CharField(max_length=20)
    route = models.CharField(max_length=30, null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_read = models.DateTimeField(null=True, blank=True)

