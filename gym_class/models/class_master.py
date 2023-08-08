from django.db import models
import datetime


class ClassMaster(models.Model):
    gym = models.ForeignKey('business.Gym', on_delete=models.CASCADE, related_name="class_masters")
    name = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    date_deleted = models.DateTimeField(null=True)

    def __str__(self):
        return self.name

    @property
    def today_class_detail(self):
        today = datetime.date.today()
        today_weekday = today.weekday()
        return self.class_details.get(day=today_weekday)

