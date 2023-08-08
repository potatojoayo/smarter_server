from django.db import models


class Faq(models.Model):
    class Meta:
        ordering = ('-date_created',)

    title = models.CharField(max_length=100)
    contents = models.TextField()
    user = models.ForeignKey('authentication.User', on_delete=models.PROTECT, related_name='faqs')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
