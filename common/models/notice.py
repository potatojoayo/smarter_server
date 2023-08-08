from django.db import models


class Notice(models.Model):
    class Meta:
        ordering = ('-date_created',)

    title = models.CharField(max_length=100)
    contents = models.TextField()
    user = models.ForeignKey('authentication.User', on_delete=models.PROTECT, related_name='notice')
    date_created = models.DateTimeField(null=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

