from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django_apscheduler.jobstores import DjangoJobStore

from gym_student.methods.gym_send_notification import gym_send_notification
from gym_student.models import AuditionDetail, AuditionMaster
from scheduler.apps import scheduler


def audition_date_alarm(audition_master_ids):
    audition_masters = AuditionMaster.objects.filter(pk__in=audition_master_ids)
    for audition_master in audition_masters:
        audition_details = AuditionDetail.objects.filter(audition_master=audition_master)
        for audition_detail in audition_details:
            student = audition_detail.student
            gym_send_notification(user=student, type="학생승급심사일 알림", audition_master=audition_master)

def audition_date_alarm_main(date_alarm, audition_master_ids, gym_id):
    now = datetime.now()
    date = str(date_alarm)
    date_year = int(date[0:4])
    date_month = int(date[5:7])
    date_day = int(date[8:10])
    date_hour = int(date[11:13])
    date_minute = int(date[14:16])
    cron_job = {'year': date_year, 'month': date_month, 'day': date_day, 'hour': date_hour, 'minute': date_minute}
    scheduler.add_job(audition_date_alarm, 'cron', **cron_job, args=[audition_master_ids], id='audition_date_alarm_'+str(gym_id)+' '+str(now), replace_existing=True)
