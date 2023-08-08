from django.db import models

from authentication.models import User
from gym_student.models.relationship import Relationship


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="parent")
    relationship = models.ForeignKey(Relationship, on_delete=models.PROTECT, related_name="parent")
    address = models.CharField(max_length=100, null=True, blank=True)
    detail_address = models.CharField(max_length=150, null=True, blank=True)
    zip_code = models.CharField(max_length=15, null=True, blank=True)
    supporter_name = models.CharField(max_length=10, null=True, blank=True)
    supporter_relationship = models.ForeignKey(Relationship, on_delete=models.PROTECT, related_name="supporter_parents", null=True, blank=True)
    supporter_phone = models.CharField(max_length=20, null=True, blank=True)
