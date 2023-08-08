from datetime import datetime

from class_payment.models import ClassPaymentMaster


def update_day_to_pay(student, old_day_to_pay, new_day_to_pay):
    print(student)
    print(student.name)
    today = datetime.today().date()
    order_id = 'C{}'.format(datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3])
    if today.day < old_day_to_pay < new_day_to_pay:
        price_to_pay = round(((new_day_to_pay - old_day_to_pay) / 30) * student.price_to_pay,-3)
        ClassPaymentMaster.objects.get_or_create(class_master=student.class_mastser,
                                                 order_id = order_id,
                                                 class_name = student.class_mastser.name,
                                                 student=student,
                                                 price=price_to_pay,
                                                 date_from = datetime(today.year, today.month, old_day_to_pay),
                                                 date_to = datetime(today.year, today.month, new_day_to_pay),
                                                 price_to_pay=price_to_pay,
                                                 date_to_pay=today,
                                                 type="원비납입일변경")
    elif old_day_to_pay < new_day_to_pay < today.day:
        price_to_pay = round((((new_day_to_pay - old_day_to_pay)/30)*student.price_to_pay),-3)
        if price_to_pay<0 :
            price_to_pay=0
        ClassPaymentMaster.objects.get_or_create(class_master=student.class_master,
                                                 order_id=order_id,
                                                 class_name=student.class_master.name,
                                                 student=student,
                                                 price=price_to_pay,
                                                 date_from = datetime(today.year, today.month+1, old_day_to_pay),
                                                 date_to = datetime(today.year, today.month+1, new_day_to_pay-1),
                                                 price_to_pay=price_to_pay,
                                                 date_to_pay=datetime(today.year, today.month+1, old_day_to_pay),
                                                 type="원비납입일변경")
    elif old_day_to_pay < today.day < new_day_to_pay:
        price_to_pay = round(((new_day_to_pay-old_day_to_pay)/30) * student.price_to_pay,-3)
        if price_to_pay < 0 :
            price_to_pay=0
        ClassPaymentMaster.objects.get_or_create(class_master=student.class_master,
                                                 order_id=order_id,
                                                 class_name=student.class_master.name,
                                                 studen=student,
                                                 price=price_to_pay,
                                                 date_from = datetime(today.year, today.month+1, old_day_to_pay),
                                                 date_to = datetime(today.year, today.month+1, new_day_to_pay-1),
                                                 price_to_pay=price_to_pay,
                                                 date_to_pay=datetime(today.year, today.month+1, old_day_to_pay),
                                                 type="원비납입일변경")
