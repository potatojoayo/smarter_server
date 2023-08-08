from django_apscheduler.jobstores import DjangoJobStore

from scheduler.apps import scheduler
from scheduler.methods import update_membership, attendance_management, calculate_agencies, calculate_subcontractors, \
    create_class_payments, absent_management
from scheduler.methods.notification_alarm_send_again import notification_alarm_send_again
from scheduler.methods.today_scheduler import today_scheduler


def run_schedulers():
    scheduler.add_jobstore(DjangoJobStore(), 'default')

    DjangoJobStore.remove_all_jobs(scheduler)

    # today_scheduler_cron = {'month': '*', 'day': '*', 'hour': '12', 'minute': '50'}
    # scheduler.add_job(today_scheduler, 'cron', **today_scheduler_cron, id='today_scheduler')



    calculate_agencies_cron = {'month': '*', 'day': '1,16', 'hour': '1', 'minute': '0'}
    scheduler.add_job(calculate_agencies, 'cron', **calculate_agencies_cron, id='calculate_agencies')

    calculate_subcontractors_cron = {'month': '*', 'day': '1,16', 'hour': '1', 'minute': '30'}
    scheduler.add_job(calculate_subcontractors, 'cron', **calculate_subcontractors_cron, id='calculate_subcontractors',
                      replace_existing=True)

    notification_alarm_send_again_cron = {'month': '*', 'day': '*', 'hour':'12', 'minute':'0'}
    scheduler.add_job(notification_alarm_send_again, 'cron', **notification_alarm_send_again_cron, id='notification_alarm_send_again',
                      replace_existing=True)


    try:
        print('스케쥴러를 시작하는 중입니다...')
        scheduler.start()
        print('스케쥴러가 시작되었습니다.')

    except KeyboardInterrupt:
        print('스케쥴러를 정지하는 중 입니다...')
        scheduler.shutdown()
        print('스케쥴러 정지되었습니다.')
