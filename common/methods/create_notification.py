
from django.contrib.auth.models import Group
from firebase_admin import messaging
from celery import shared_task

from authentication.models import User
from common.models import Notification
from server.celery import logger
from server.settings import parents_app, default_app

@shared_task
def create_notification(user_id, notification_type, title, contents, route=None, payload=None):
    user = User.objects.get(pk=user_id)
    logger.info('create_notification')
    logger.info('user_name : '+str(user.name))
    logger.info('before_notification_type : '+str(notification_type))
    Notification.objects.create(
        user_id=user.id,
        notification_type=notification_type,
        title=title,
        contents=contents,
        route=route,
    )

    if len(user.fcm_tokens) > 0:
        logger.info('fcm_tokens ok')
        logger.info('in_notification_type : '+str(notification_type))
        logger.info('user : '+str(user))
        logger.info('title : '+str(title))
        logger.info('contents : '+str(contents))

        badge = Notification.objects.filter(user=user, date_read__isnull=True).count()
        parent = Group.objects.get(name='학부모')
        if user in parent.user_set.all():
            app = parents_app
        else:
            app = default_app

        logger.info('app_name : '+str(app.name))
        logger.info('---alarm---')

        message = messaging.MulticastMessage(
            tokens=user.fcm_tokens,
            notification=messaging.Notification(
                title=title,
                body=contents,
            ),
            apns=messaging.APNSConfig(
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(
                        badge=badge,
                        sound='files/sounds/alarm_sound.mp3',
                    )
                )
            )
        )
        response = messaging.send_multicast(message, app=app)
        logger.info('response : '+str(response))
        logger.info('success_response_number : ' + str(response.success_count))
        logger.info('failure_response_number : ' + str(response.failure_count))

