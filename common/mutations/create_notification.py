import graphene
from common.types.notification_type import NotificationType
from common.methods.create_notification import create_notification


class CreateNotification(graphene.Mutation):
    class Arguments:
        notification_type = graphene.Int(required=True)
        title = graphene.String(required=True)
        contents = graphene.String(required=True)

    notification = graphene.Field(NotificationType)

    @classmethod
    def mutate(cls,
               _,
               info,
               notification_type,
               title,
               contents):

        create_notification(user=info.context.user,
                            notification_type=notification_type,
                            title=title,
                            contents=contents,
                            )



