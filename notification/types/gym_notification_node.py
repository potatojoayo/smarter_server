import os

import graphene
from graphene_django import DjangoObjectType
from graphene import relay

from base_classes import CountableConnectionBase
from notification.models.gym_notification import GymNotification


class GymNotificationNode(DjangoObjectType):

    class Meta:
        model = GymNotification
        interfaces = (relay.Node,)
        filter_fields = {
            'title' : ['icontains']
        }
        connection_class = CountableConnectionBase

    notification_id = graphene.Int()
    images = graphene.List(graphene.String)

    @staticmethod
    def resolve_notification_id(root, __):
        return root.id

    @staticmethod
    def resolve_images(root, _):
        images = []
        for i in root.images.all():
            images.append(os.environ.get("BASE_URL") + i.image.url)
        return images
