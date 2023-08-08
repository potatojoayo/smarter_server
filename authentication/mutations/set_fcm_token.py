import graphene
from django.contrib.auth.models import AnonymousUser

from authentication.models import User


class SetFcmToken(graphene.Mutation):

    class Arguments:
        fcm_token = graphene.String()
        identification = graphene.String()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, info, fcm_token, identification=None):
        if identification:
            user = User.objects.get(identification=identification)
        else:
            user = info.context.user
        if user is AnonymousUser:
            return SetFcmToken(success=False)
        if fcm_token not in user.fcm_tokens:
            if len(user.fcm_tokens) == 5:
                user.fcm_tokens.remove(user.fcm_tokens[0])
            user.fcm_tokens.append(fcm_token)
        user.save()
        return SetFcmToken(success=True)

