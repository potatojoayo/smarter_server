from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django_apscheduler.jobstores import DjangoJobStore

from gym_student.methods.gym_send_notification import gym_send_notification
from notification.models import GymNotification
from notification.models.gym_notification_receiver import GymNotificationReceiver
from scheduler.apps import scheduler


def set_alarm_for_notification(parent_list, title, gym_notification_id):
    gym_notification = GymNotification.objects.get(pk=gym_notification_id)
    for parent in parent_list:
        print(parent)
        GymNotificationReceiver.objects.create(gym_notification=gym_notification,
                                               parent=parent['student'].parent)
        gym_send_notification(user=parent['student'], type="알림장알림", gym_notification_title=title)




def set_alarm_for_notification_main(send_time, parent_list, title, gym_id, gym_notification_id):
    send_time = str(send_time)
    date_year = int(send_time[0:4])
    date_month = int(send_time[5:7])
    date_day = int(send_time[8:10])
    date_hour = int(send_time[11:13])
    date_minute = int(send_time[14:16])
    cron_job = {'year': date_year,'month': date_month, 'day': date_day, 'hour': date_hour, 'minute': date_minute}
    scheduler.add_job(set_alarm_for_notification, 'cron', **cron_job, args=[parent_list, title, gym_notification_id], id='set_alarm_for_notification'+str(gym_id)+''+str(gym_notification_id), replace_existing=True)
