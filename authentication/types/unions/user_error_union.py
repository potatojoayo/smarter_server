import graphene

from authentication.types import UserType
from authentication.errors import CredentialError


class UserErrorUnion(graphene.Union):
    class Meta:
        types = (UserType, CredentialError,)

