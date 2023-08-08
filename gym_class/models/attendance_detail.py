from django.db import models

from gym_class.models import AttendanceMaster
from gym_student.models import Student


class AttendanceDetail(models.Model):
    attendance_master = models.ForeignKey(AttendanceMaster, on_delete=models.CASCADE, related_name="attendance_details")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendance_details")
    type = models.CharField(max_length=15, null=True, blank=True)
    date_attended = models.DateTimeField(null=True)
    absent_reason = models.CharField(null=True, max_length=200, blank=True)

    def __str__(self):
        return '{} - {} - {} -{} -{}'.format(self.student, self.type, self.attendance_master.class_master.name, self.attendance_master.class_detail.hour_start, self.attendance_master.class_detail.min_start)