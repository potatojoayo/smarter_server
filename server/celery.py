import os
import datetime
from celery import Celery
from celery.schedules import crontab
from celery.signals import setup_logging
from django.conf import settings

from server.settings import BASE_DIR

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

app = Celery("server")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.update(
    BROKER_URL='django://',
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Seoul',
    CELERY_ENABLE_UTC=False,
    CELERYBEAT_SCHEDULE = {
        'today_scheduler': {
        'task': 'scheduler.methods.today_scheduler.today_scheduler',
        'schedule': crontab(hour='0', minute='0'),
        'args': ()
        },
        'calculate_agencies':{
            'task': 'scheduler.methods.calculate_agencies.calculate_agencies',
            'schedule':crontab(day_of_month='1,16', hour='0', minute='15'),
            'args':()
        },
        'calculate_subcontractor':{
            'task': 'scheduler.methods.calculate_subcontractor.calculate_subcontractor',
            'schedule':crontab(day_of_month='1,16', hour='0', minute='30'),
            'args':()
        },
        'notification_alarm_send_again':{
            'task': 'scheduler.methods.notification_alarm_send_again.notification_alarm_send_again',
            'schedule':crontab(hour='12', minute='0')
        },
        'calculate_gym_purchased_amount':{
            'task': 'scheduler.methods.calculate_gym_purchased_amount.calculate_gym_purchased_amount',
            'schedule':crontab(day_of_month='1', hour='1', minute='0')
        }
    }
)
import logging

# Create a logger
logger = logging.getLogger(__name__)

# Set the log level
logger.setLevel(logging.DEBUG)

# Create a file handler for the logger
log_file_path = BASE_DIR.joinpath('logs', f'celery_log_{datetime.datetime.now().strftime("%Y-%m-%d")}.log')
fh = logging.FileHandler(log_file_path)

# Set the log level for the file handler
fh.setLevel(logging.DEBUG)

# Create a formatter for the log messages
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Set the formatter for the file handler
fh.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(fh)


app.autodiscover_tasks(['common.methods.create_notification.create_notification',
                        'authentication.methods.solapi_async_message.solapi_async_message',
                        'scheduler.methods.today_scheduler.today_scheduler',
                        'scheduler.methods.calculate_agencies.calculate_agencies',
                        'scheduler.methods.calculate_subcontractors.calculate_subcontractors',
                        'scheduler.methods.notification_alarm_send_again.notification_alarm_send_again',
                        'gym_student.methods.send_notification_installation.send_notification_installation',
                        'cs.methods.issued_to_filter.issued_to_filter',
                        'cs.methods.coupon_methods.issue_coupon.issue_coupon',
                        'cs.methods.coupon_methods.issue_referral_coupon.referral_coupon'])



# result = app.send_task('scheduler.methods.run_schedulers.run_schedulers')
# task_id = result.task_id
#
# # Later, if you want to revoke the task
# app.control.revoke(task_id, terminate=True)
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
    logger.debug("Starting my_task")
    # Your task code here
    logger.debug("Finished my_task")