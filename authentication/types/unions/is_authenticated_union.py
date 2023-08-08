import graphene

from authentication.errors import CredentialError
from authentication.types import AuthenticationOkType


class IsAuthenticatedUnion(graphene.Union):
    class Meta:
        types = (AuthenticationOkType, CredentialError,)
