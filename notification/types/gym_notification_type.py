import graphene
from graphene_django import DjangoObjectType
from graphene import relay
from notification.models.gym_notification import GymNotification


class GymNotificationType(DjangoObjectType):
    notification_receivers = graphene.String(source='notification_receivers')
    class Meta:
        model = GymNotification
        interface = (relay.Node,)
