import graphene

from gym_student.methods.gym_send_notification import gym_send_notification
from notification.models import GymNotification
from notification.models.gym_notification_receiver import GymNotificationReceiver


class SendNotificationAlarmAgain(graphene.Mutation):
    class Arguments:
        gym_notification_ids = graphene.List(graphene.Int)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, gym_notification_ids):
        gym_notifications = GymNotification.objects.filter(pk=gym_notification_ids)
        for gym_notification in gym_notifications:
            gym_notification_receivers = GymNotificationReceiver.objects.filter(gym_notification=gym_notification,
                                                                            date_read=None)
            print(gym_notification_receivers)
            for gym_notification_receiver in gym_notification_receivers:
                gym_send_notification(user=gym_notification_receiver, type="알림장알림", gym_notification_title=gym_notification.title)

        return SendNotificationAlarmAgain(success=True)