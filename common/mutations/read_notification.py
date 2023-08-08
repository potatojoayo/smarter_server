from django.utils import timezone
import graphene
from common.models import Notification


class ReadNotification(graphene.Mutation):

    class Arguments:
        notification_id = graphene.Int()

    success = graphene.Boolean(default_value=True)

    @classmethod
    def mutate(cls, _, __, notification_id):
        Notification.objects.filter(pk=notification_id).update(date_read=timezone.now())
        return ReadNotification(success=True)




