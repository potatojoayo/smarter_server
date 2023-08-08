from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore

from business.models import Gym
from class_payment.models import ClassPaymentMaster
from gym_class.models import ClassMaster
from gym_student.methods.gym_send_notification import gym_send_notification
from scheduler.apps import scheduler
from server import settings


def alarm_for_class_payments(class_payment_master_ids):
    class_payment_masters = ClassPaymentMaster.objects.filter(pk__in=class_payment_master_ids)
    for class_payment_master in class_payment_masters:
        gym_send_notification(user=class_payment_master.student, type="학원비 알림")

def alarm_for_class_payments_main(class_payment_master_ids ,date, gym_id):
    now = datetime.now()
    date = str(date)
    date_year = int(date[0:4])
    date_month = int(date[5:7])
    date_day = int(date[8:10])
    date_hour = int(date[11:13])
    date_minute = int(date[14:16])
    cron_job = {'year': date_year, 'month': date_month, 'day': date_day, 'hour': date_hour, 'minute': date_minute}
    scheduler.add_job(alarm_for_class_payments, 'cron', **cron_job, args=[class_payment_master_ids], id='alarm_for_class_payments'+str(gym_id)+' '+str(now), replace_existing=True)
