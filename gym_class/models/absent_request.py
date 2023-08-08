from django.db import models

from gym_student.models import Student


class AbsentRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="absent_requests")
    type = models.CharField(max_length=20)
    absent_reason = models.CharField(max_length=30)
    date_created = models.DateTimeField(auto_now_add=True)
    date_absent = models.DateTimeField()

    def __str__(self):
        '{}. {} {} '.format(self.student.name, self.type, self.absent_reason)


