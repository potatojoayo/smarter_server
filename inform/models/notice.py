from django.db import models


class Notice(models.Model):

    writer = models.ForeignKey('authentication.User', on_delete=models.PROTECT, related_name='notices')
    title = models.CharField(max_length=100)
    contents = models.TextField()
    is_active = models.BooleanField(default=True)

    # DATE
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

