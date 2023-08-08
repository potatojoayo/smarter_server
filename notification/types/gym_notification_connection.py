from graphene import relay

from notification.types.gym_notification_type import GymNotificationType


class GymNotificationConnection(relay.Connection):
    class Meta:
        node = GymNotificationType
