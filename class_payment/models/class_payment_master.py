from django.db import models

from gym_class.models import ClassMaster
from gym_student.models import Student


class ClassPaymentMaster(models.Model):
    class_master = models.ForeignKey(ClassMaster, on_delete=models.PROTECT, related_name="class_payment_masters")
    class_name = models.CharField(max_length=100,)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="class_payment_masters")
    price = models.IntegerField() ## 차감전 원비
    date_paid = models.DateField(null=True, blank=True)
    date_from = models.DateField()
    date_to = models.DateField()
    type = models.CharField(max_length=15, null=True)
    price_deduct = models.IntegerField(default=0)
    days_deduct = models.IntegerField(default=0)
    order_id = models.CharField(max_length=25, unique=True)
    date_to_pay = models.DateField(null=True, blank=True)
    price_to_pay = models.IntegerField() ## 차감후 원비
    payment_method = models.CharField(max_length=15, default="미납")
    payment_status = models.CharField(default="미납", max_length=5)
    is_approved = models.BooleanField(default=False)
    memo = models.TextField(null=True)
