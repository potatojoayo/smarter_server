from django.db import models

from gym_class.models import ClassMaster
from gym_class.models.level import Level
from gym_student.models.parent import Parent
from gym_student.models.school import School


class Student(models.Model):

    class_master = models.ForeignKey(ClassMaster, on_delete=models.PROTECT, related_name="students")
    level = models.ForeignKey(Level, on_delete=models.PROTECT, related_name="students")
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name="students")
    school = models.ForeignKey(School, on_delete=models.PROTECT, related_name="students")
    name = models.CharField(max_length=15)
    birthday = models.DateField()
    status = models.CharField(max_length=15)
    phone = models.CharField(max_length=20)
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    date_entered = models.DateField()
    class_date_start = models.DateField(null=True)
    day_to_pay = models.IntegerField()
    gender = models.CharField(max_length=5)
    is_deleted = models.BooleanField(default=False)
    date_exit = models.DateField(null=True, blank=True)
    price_to_pay = models.IntegerField(null=True)
    memo_for_health = models.TextField(null=True)
    memo_for_price = models.TextField(null=True)
    memo = models.TextField(null=True)

    def __str__(self):
        return self.name + ' - ' + self.parent.user.name
