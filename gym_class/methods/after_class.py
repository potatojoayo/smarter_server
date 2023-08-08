import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django_apscheduler.jobstores import DjangoJobStore

from gym_class.models import AttendanceDetail
from gym_student.methods.gym_send_notification import gym_send_notification


def after_class():
    today = datetime.date.today()
    now = datetime.datetime.now()
    class_finished_time = now + datetime.timedelta(minutes=-15)
    attendances = AttendanceDetail.objects.filter(attendance_master__class_detail__hour_end=class_finished_time.hour,
                                                  attendance_master__class_detail__min_end=class_finished_time.minute,
                                                  attendance_master__date=today).exclude(type="결석")
    attendances.update(type="하원")
    # for attendance in attendances:
    #     gym_send_notification(user=attendance.student, type="하원알림", attendance_hour=now.hour, attendance_min=now.minute)


def after_class_main():
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    cron_job = {'month': '*', 'day': '*', 'hour': '*', 'minute': '5'}
    scheduler.add_job(after_class, 'cron', **cron_job, id='after_class_001', replace_existing=True)
