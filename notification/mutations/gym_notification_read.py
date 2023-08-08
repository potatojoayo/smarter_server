from datetime import datetime

import graphene

from notification.models.gym_notification_receiver import GymNotificationReceiver


class GymNotificationRead(graphene.Mutation):
    class Arguments:
        gym_notification_receiver_id = graphene.Int()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, gym_notification_receiver_id):
        now = datetime.now()
        gym_notification_receiver = GymNotificationReceiver.objects.get(pk=gym_notification_receiver_id)
        gym_notification_receiver.date_read = now
        gym_notification_receiver.save()

        return GymNotificationRead(success=True)
