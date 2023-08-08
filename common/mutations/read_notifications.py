from firebase_admin import messaging
from datetime import datetime
import graphene
from common.models import Notification


class ReadNotifications(graphene.Mutation):

    success = graphene.Boolean(default_value=True)

    @classmethod
    def mutate(cls, _, info):

        user = info.context.user
        now = datetime.now()
        Notification.objects.filter(user=user).update(
            date_read=now
        )

        message = messaging.MulticastMessage(
            tokens=user.fcm_tokens,
            android=messaging.AndroidConfig(
                notification=messaging.AndroidNotification(
                    notification_count=0,
                )
            ),
            apns=messaging.APNSConfig(
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(
                        content_available=1,
                        badge=0,
                    )
                )
            )
        )

        response = messaging.send_multicast(message)
        print(response)

        return ReadNotifications()




