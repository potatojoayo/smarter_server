from datetime import datetime

from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta

from class_payment.models import ClassPaymentMaster


def create_class_payment(student):
    now = datetime.now()
    order_id = 'C{}'.format(datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3])
    print(now.weekday())
    print(now.day)
    print(student.day_to_pay)
    if now.day <= student.day_to_pay:
        date_to_pay = datetime(year=now.year, month=now.month, day=student.day_to_pay)
    else:
        if now.year == 12:
            date_to_pay = datetime(year=now.year+1, month=1, day=student.day_to_pay)
        else:
            date_to_pay = datetime(year=now.year, month=now.month+1, day=student.day_to_pay)
    # pay_date = date_to_pay if date_to_pay > now else date_to_pay + relativedelta(months=1)
    pay_date_from = student.class_date_start
    print(date_to_pay)
    if (student.class_date_start - date_to_pay.date()).days > 0 :
        print(1)
        if now.month == date_to_pay.month :
            pay_date_to = datetime(year=now.year, month=student.class_date_start.month ,day=student.day_to_pay) + timedelta(days=-1)
            price = round((abs((pay_date_from - (pay_date_to + timedelta(days=1)).date()).days) / 30) * student.price_to_pay, -3)
            ClassPaymentMaster.objects.create(class_master=student.class_master,
                                              order_id=order_id,
                                              class_name=student.class_master.name,
                                              student=student,
                                              price=student.price_to_pay,
                                              date_from=student.class_date_start,
                                              date_to=pay_date_to,
                                              price_deduct=0,
                                              days_deduct=0,
                                              price_to_pay=price,
                                              date_to_pay=now.date(),
                                              type="신규")
        else:
            pay_date_to = datetime(year=now.year, month=student.class_date_start.month + 1,
                                   day=student.day_to_pay) + timedelta(days=-1)
            price = round((abs((pay_date_from - (pay_date_to + timedelta(days=1)).date()).days) / 30) * student.price_to_pay, -3)
            ClassPaymentMaster.objects.create(class_master=student.class_master,
                                              order_id=order_id,
                                              class_name=student.class_master.name,
                                              student=student,
                                              price=student.price_to_pay,
                                              date_from=student.class_date_start,
                                              date_to=pay_date_to,
                                              price_deduct=0,
                                              days_deduct=0,
                                              price_to_pay=price,
                                              date_to_pay=now.date(),
                                              type="신규")
    elif (date_to_pay.date() - student.class_date_start ).days == 1:
        ClassPaymentMaster.objects.create(class_master=student.class_master,
                                          order_id=order_id,
                                          class_name=student.class_master.name,
                                          student=student,
                                          price=round(student.price_to_pay/30, -3),
                                          date_from=student.class_date_start,
                                          date_to=student.class_date_start,
                                          price_deduct=0,
                                          days_deduct=0,
                                          price_to_pay=round(student.price_to_pay/30, -3),
                                          date_to_pay=now.date(),
                                          type="신규")

        pay_date_to = datetime(year=now.year, month=now.month , day=student.day_to_pay) + relativedelta(months=+1) + timedelta(days=-1)
        order_id_2 = 'C{}'.format(datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3])

        ClassPaymentMaster.objects.create(class_master=student.class_master,
                                          order_id=order_id_2,
                                          class_name=student.class_master.name,
                                          student=student,
                                          price=student.price_to_pay,
                                          date_from=student.class_date_start + timedelta(days=1),
                                          date_to=pay_date_to,
                                          price_deduct=0,
                                          days_deduct=0,
                                          price_to_pay=student.price_to_pay,
                                          date_to_pay=now.date(),
                                          type="정기")
    elif (student.class_date_start - date_to_pay.date()).days == 0:
        pay_date_to = student.class_date_start + relativedelta(months=+1) + timedelta(days=-1)
        ClassPaymentMaster.objects.create(class_master=student.class_master,
                                          order_id=order_id,
                                          class_name=student.class_master.name,
                                          student=student,
                                          price=student.price_to_pay,
                                          date_from=student.class_date_start,
                                          date_to=pay_date_to,
                                          price_deduct=0,
                                          days_deduct=0,
                                          price_to_pay=student.price_to_pay,
                                          date_to_pay=now.date(),
                                          type="신규")

    else:
        if student.class_date_start.month == now.month :
            print(4)
            # pay_date_to = datetime(year=now.year, month=now.month, day=student.day_to_pay) + timedelta(days=-1)
            pay_date_to = date_to_pay + timedelta(days=-1)
            price = round((abs((pay_date_from - date_to_pay.date()).days) / 30) * student.price_to_pay, -3)
            ClassPaymentMaster.objects.create(class_master=student.class_master,
                                              order_id=order_id,
                                              class_name=student.class_master.name,
                                              student=student,
                                              price=student.price_to_pay,
                                              date_from=student.class_date_start,
                                              date_to=pay_date_to,
                                              price_deduct=0,
                                              days_deduct=0,
                                              price_to_pay=price,
                                              date_to_pay=now.date(),
                                              type="신규")
        else:
            pay_date_to = datetime(year=now.year, month=now.month + 1, day=student.day_to_pay) + timedelta(days=-1)
            print(5)
            print(pay_date_to)
            price = round((abs((pay_date_from - date_to_pay.date()).days) / 30) * student.price_to_pay, -3)
            ClassPaymentMaster.objects.create(class_master=student.class_master,
                                              order_id=order_id,
                                              class_name=student.class_master.name,
                                              student=student,
                                              price=student.price_to_pay,
                                              date_from=student.class_date_start,
                                              date_to=pay_date_to,
                                              price_deduct=0,
                                              days_deduct=0,
                                              price_to_pay=price,
                                              date_to_pay=now.date(),
                                              type="신규")
