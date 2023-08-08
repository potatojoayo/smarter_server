from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django_apscheduler.jobstores import DjangoJobStore

from gym_student.methods.gym_send_notification import gym_send_notification
from gym_student.models import AuditionMaster, AuditionDetail
from scheduler.apps import scheduler


def audition_result_alarm(audition_master_id):
    audition_master = AuditionMaster.objects.get(pk=audition_master_id)
    audition_details = AuditionDetail.objects.filter(audition_master=audition_master)
    for audition_detail in audition_details:
        did_pass = audition_detail.did_pass
        if did_pass:
            gym_send_notification(user=audition_detail.student.parent.user, type="승급 완료 알림", audition_detail=audition_detail)
        else:
            gym_send_notification(user=audition_detail.student.parent.user, type="승급 실패 알림", audition_detail=audition_detail)




def audition_result_alarm_main(estimated_alarm_date, audition_master_id, gym_id):
    now = datetime.now()
    date = str(estimated_alarm_date)
    date_year = int(date[0:4])
    date_month = int(date[5:7])
    date_day = int(date[8:10])
    date_hour = int(date[11:13])
    date_minute = int(date[14:16])
    cron_job = {'year': date_year,'month': date_month, 'day': date_day, 'hour': date_hour, 'minute': date_minute}
    scheduler.add_job(audition_result_alarm, 'cron', **cron_job, args=[audition_master_id], id='audition_result_alarm_'+str(gym_id)+' '+str(now), replace_existing=True)
