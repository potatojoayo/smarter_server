import graphene
import graphql_jwt
from graphql_jwt.decorators import token_auth
from graphql_jwt.utils import get_payload

from authentication.models import User
from authentication.types import UserType


class VerifyToken(graphql_jwt.Verify):
    class Arguments:
        fcm_token = graphene.String()
        token = graphene.String()

    user = graphene.Field(UserType)
    is_active = graphene.Boolean(default_value=False)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        token = kwargs.get('token')
        pay_load = get_payload(token, info.context)
        user = User.objects.get(identification=pay_load['identification'])
        if 'fcm_token' in kwargs:
            fcm_token = kwargs.get('fcm_token')
            if fcm_token not in user.fcm_tokens:
                if len(user.fcm_tokens) == 5:
                    user.fcm_tokens.remove(user.fcm_tokens[0])
                user.fcm_tokens.append(fcm_token)
            user.save()
        return cls(user=user, is_active=user.is_active, payload=pay_load)

