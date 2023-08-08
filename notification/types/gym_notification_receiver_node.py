from graphene_django import DjangoObjectType
from graphene import relay
import graphene
from base_classes import CountableConnectionBase
from notification.models.gym_notification_receiver import GymNotificationReceiver


class GymNotificationReceiverNode(DjangoObjectType):
    class Meta:
        model = GymNotificationReceiver
        interfaces = (relay.Node,)
        filter_fields = {}
        connection_class = CountableConnectionBase

    receiver_id = graphene.Int()

    @staticmethod
    def resolve_receiver_id(root, __):
        return root.id