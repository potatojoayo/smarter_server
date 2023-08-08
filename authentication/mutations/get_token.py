import graphene
import graphql_jwt

from authentication.types import UserType


class ObtainJsonWebToken(graphql_jwt.JSONWebTokenMutation):

    class Arguments:
        fcm_token = graphene.String()

    user = graphene.Field(UserType)
    is_active = graphene.Boolean(default_value=False)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        user = info.context.user
        if 'fcm_token' in kwargs:
            fcm_token = kwargs.get('fcm_token')
            if fcm_token not in user.fcm_tokens:
                if len(user.fcm_tokens) == 5:
                    user.fcm_tokens.remove(user.fcm_tokens[0])
                user.fcm_tokens.append(fcm_token)
            user.save()
        return cls(user=user, is_active=user.is_active)
