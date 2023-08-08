import graphene

from error.base_error import BaseError


class CredentialError(graphene.ObjectType):
    class Meta:
        interfaces = (BaseError, )

    error_message = graphene.String(default_value='아이디 또는 비밀번호를 다시 확인해주세요.', required=True)
