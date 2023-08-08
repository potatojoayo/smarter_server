from graphene import relay

from notification.types.gym_notification_receiver_type import GymNotificationReceiverType


class GymNotificationReceiverConnection(relay.Connection):
    class Meta:
        node = GymNotificationReceiverType