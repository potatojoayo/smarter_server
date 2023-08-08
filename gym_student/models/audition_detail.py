from django.db import models

from gym_student.models.audition_master import AuditionMaster
from gym_student.models.student import Student


class AuditionDetail(models.Model):
    audition_master = models.ForeignKey(AuditionMaster, on_delete=models.CASCADE, related_name="audition_details")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="audition_details")
    did_pass = models.BooleanField(null=True)
    memo = models.TextField(null=True)