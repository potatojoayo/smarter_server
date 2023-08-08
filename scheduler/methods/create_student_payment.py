from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from class_payment.models import ClassPaymentMaster
from gym_student.models import Student


def create_student_payment(month, day):
    print('creat_student_payment')
    print(month)
    print(day)
    today = datetime(2023, month, day).date()
    print(today)
    pay_date = today + timedelta(days=1)
    pay_day = pay_date.day
    pay_date_from = pay_date
    pay_date_to = pay_date_from + relativedelta(months=1) + timedelta(days=-1)
    ex_class_date_from = today + relativedelta(months=-1)

    if today.month == 2 and pay_day == 29:
        students = Student.objects.filter(day_to_pay=pay_day, is_deleted=False, status="수강중") \
                   | Student.objects.filter(day_to_pay=30, is_deleted=False, status="수강중")
    elif today.month == 2 and pay_day == 28:
        pay_date_two = today + timedelta(days=2)
        if pay_date_two.day == 29:
            students = Student.objects.filter(day_to_pay=pay_day, is_deleted=False, status="수강중")
        else:
            students = Student.objects.filter(day_to_pay=pay_day, is_deleted=False, status="수강중") \
                       | Student.objects.filter(day_to_pay=29, is_deleted=False, status="수강중") \
                       | Student.objects.filter(day_to_pay=30, is_deleted=False, status="수강중")
    else:
        students = Student.objects.filter(day_to_pay=pay_day, is_deleted=False, status="수강중")
    for student in students:
        if student.class_date_start is None or student.class_date_start < pay_date:
            if student.class_date_start == today or student.class_date_start == today + timedelta(days=-1):
                pass
            else:
                order_id = 'C{}'.format(datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3])
                ClassPaymentMaster.objects.get_or_create(class_master=student.class_master,
                                                         order_id=order_id,
                                                         class_name=student.class_master.name,
                                                         student=student,
                                                         price=student.price_to_pay,
                                                         date_from=pay_date_from,
                                                         date_to=pay_date_to,
                                                         price_to_pay=student.price_to_pay,
                                                         date_to_pay=pay_date,
                                                         type="정기")
