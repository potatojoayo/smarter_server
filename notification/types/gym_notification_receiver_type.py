from graphene_django import DjangoObjectType
from graphene import relay
from notification.models.gym_notification_receiver import GymNotificationReceiver


class GymNotificationReceiverType(DjangoObjectType):
    class Meta:
        model = GymNotificationReceiver
        interface = (relay.Node,)
