from django.db import models
from business.models import Gym
from gym_class.models import ClassMaster


class GymNotification(models.Model):
    class_master = models.ForeignKey(ClassMaster, on_delete=models.PROTECT, related_name="gym_notifications", null=True)
    gym = models.ForeignKey(Gym, on_delete=models.PROTECT, related_name="gym_notifications")
    title = models.CharField(max_length=50)
    contents = models.CharField(max_length=3000)
    type = models.CharField(max_length=20,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    send_type = models.CharField(max_length=10, null=True) # 예약 or 즉시
    send_datetime = models.DateTimeField(null=True)
    event_date = models.DateField(null=True)

    @property
    def notification_receivers(self):
        notification_receivers = self.receivers.all()
        receivers_first = notification_receivers.first()
        receivers_first = receivers_first.parent.students.first()
        receivers_first_name = receivers_first.name
        receivers_number = notification_receivers.count() - 1
        if self.type == "전체":
            return "전체"
        elif self.type == "클래스":
            return "{} 학생, 학부모님".format(self.class_master.name)
        if receivers_number == 0:
            return "{}, {} 학부모님".format(receivers_first_name, receivers_first_name)
        return "{} 외 {}명, 해당학생 학부모님".format(receivers_first_name, receivers_number)
