import datetime

from gym_student.methods.gym_send_notification import gym_send_notification
from notification.models import GymNotification
from server.celery import app, logger


@app.task
def notification_alarm_send_again():
    logger.info('staring notification_alarm_send_again')
    today = datetime.datetime.today().date()
    today_plus_one = today + datetime.timedelta(days=1)
    print(today)
    print(today_plus_one)
    gym_notifications = GymNotification.objects.filter(event_date=today_plus_one).exclude(send_datetime__year=today_plus_one.year,
                                                                                          send_datetime__month=today_plus_one.month,
                                                                                          send_datetime__day=today_plus_one.day)
    logger.info('gym_notifications')
    logger.info(gym_notifications)

    for gym_notification in gym_notifications:
        gym_notification_receivers = gym_notification.receivers.all()
        for gym_notification_receiver in gym_notification_receivers:
            gym_send_notification(user=gym_notification_receiver.parent.user, type="알림장알림", gym_notification_title=gym_notification.title)


