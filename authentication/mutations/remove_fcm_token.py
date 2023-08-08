import graphene

from authentication.models import User


class RemoveFcmToken(graphene.Mutation):

    class Arguments:
        fcm_token = graphene.String()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, info, fcm_token):
        user = info.context.user
        print(fcm_token)
        if fcm_token in user.fcm_tokens:
            user.fcm_tokens.remove(fcm_token)
            print(user.fcm_tokens)
            user.save()
        return RemoveFcmToken(success=True)

