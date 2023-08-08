from graphene_django import DjangoObjectType

from common.models.notification import Notification


class NotificationType(DjangoObjectType):
    class Meta:
        model = Notification
