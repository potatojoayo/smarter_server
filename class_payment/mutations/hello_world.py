import graphene
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

from class_payment.models import ClassPaymentMaster
from gym_class.models import AttendanceDetail
from gym_student.methods.gym_send_notification import gym_send_notification
from gym_student.models import Student


class HelloWorld(graphene.Mutation):
    class Arguments:
        number = graphene.Int()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, number):
        today = datetime.today().date()
        pay_date = today + timedelta(days=1)
        pay_day = pay_date.day
        pay_date_from = pay_date
        pay_date_to = pay_date_from + relativedelta(months=1) + timedelta(days=-1)
        ex_class_date_from = today + relativedelta(months=-1)
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
        ## 학생들 결석일 골라내기
        for student in students:
            absent_number = 0  # 결석 날짜 일주
            bad_absent = 0  # 무단결석 날짜 일수
            attendances = AttendanceDetail.objects.filter(student=student,
                                                          attendance_master__date__range=[ex_class_date_from,
                                                                                          today])
            for attendance in attendances:
                if attendance.type == "결석":
                    absent_number += 1
                    if attendance.absent_reason == "무단결석":
                        bad_absent += 1
            order_id = 'C{}'.format(datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3])
            ClassPaymentMaster.objects.get_or_create(class_master=student.class_master,
                                                     order_id=order_id,
                                                     class_name=student.class_master.name,
                                                     student=student,
                                                     price=student.price_to_pay,
                                                     date_from=pay_date_from,
                                                     date_to=pay_date_to,
                                                     days_deduct=absent_number,
                                                     price_to_pay=student.price_to_pay,
                                                     date_to_pay=pay_date,
                                                     memo="무단결석일수는 {}일입니다".format(bad_absent))
            gym_send_notification(user=student, type="학원비 청구서 발급")
