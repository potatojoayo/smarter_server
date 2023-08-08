import graphene
from graphene_django import DjangoObjectType
from graphene import relay
from base_classes import CountableConnectionBase

from common.models.notification import Notification


class NotificationNode(DjangoObjectType):
    class Meta:
        model = Notification
        interfaces = (relay.Node,)
        filter_fields = {
            "user__id": ['exact'],
            'user__groups__name': ['icontains'],
            "date_created": ["lte", 'gte', 'exact'],
            "notification_type": ['in']
        }
        connection_class = CountableConnectionBase

    notification_id = graphene.Int()

    @staticmethod
    def resolve_notification_id(root, _):
        return root.id

