import graphene

from ok.base_ok import BaseOk


class AuthenticationOkType(graphene.ObjectType):

    class Meta:
        interfaces = (BaseOk,)

    ok_message = graphene.String(required=True)
