from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django_apscheduler.jobstores import DjangoJobStore

from class_payment.models import ClassPaymentMaster
from gym_class.models import ClassMaster, AttendanceDetail
from gym_student.methods.gym_send_notification import gym_send_notification
from gym_student.models import Student


def create_class_payments():
    today = datetime.today().date()
    pay_date = today + timedelta(days=1)
    pay_day = pay_date.day
    pay_date_from = pay_date
    pay_date_to = pay_date_from + relativedelta(months=1) + timedelta(days=-1)
    ex_class_date_from = today + relativedelta(months=-1)
    student_attendance_list = []

    if today.month == 2 and pay_day == 29:
        students = Student.objects.filter(day_to_pay=pay_day, is_deleted=False) \
                   | Student.objects.filter(day_to_pay=30, is_deleted=False)
    elif today.month == 2 and pay_day == 28:
        pay_date_two = today + timedelta(days=2)
        if pay_date_two.day == 29:
            students = Student.objects.filter(day_to_pay=pay_day, is_deleted=False)
        else:
            students = Student.objects.filter(day_to_pay=pay_day, is_deleted=False) \
                       | Student.objects.filter(day_to_pay=29, is_deleted=False) \
                       | Student.objects.filter(day_to_pay=30, is_deleted=False)
    else:
        students = Student.objects.filter(day_to_pay=pay_day, is_deleted=False)

    for student in students:
        order_id = 'C{}'.format(datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3])
        ClassPaymentMaster.objects.get_or_create(class_master=student.class_master,
                                                 order_id=order_id,
                                                 class_name=student.class_master.name,
                                                 student=student,
                                                 price=student.price_to_pay,
                                                 date_from=pay_date_from,
                                                 date_to=pay_date_to,
                                                 price_to_pay=student.price_to_pay,
                                                 date_to_pay=pay_date)


