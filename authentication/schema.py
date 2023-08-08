import graphql_jwt
from django.contrib.auth.hashers import check_password
from graphql_jwt.decorators import login_required
import graphene

from business.models import Subcontractor
from .mutations import CheckIsActive
from .mutations.change_pasword import ChangePassword
from .mutations.check_code import CheckCode
from .mutations.check_is_admin import CheckIsAdmin
from .mutations.check_is_parent import CheckIsParent
from .mutations.check_is_ta import CheckIsTa
from .mutations.create_or_update_admin import CreateOrUpdateAdmin
from .mutations.remove_fcm_token import RemoveFcmToken
from .mutations.send_code import SendCode
from .mutations.set_fcm_token import SetFcmToken
from .mutations.set_password import SetPassword
from .mutations.upload_profile_image import UploadProfileImage
from .mutations.verify_token import VerifyToken
from .mutations.withdraw import Withdraw
from .types import UserType
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from authentication.mutations.get_token import ObtainJsonWebToken
from authentication.types.user_node import UserNode


class Query(graphene.ObjectType):
    me = graphene.Field(UserType, token=graphene.String())
    user = relay.Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode)
    is_right_password = graphene.Boolean(password=graphene.String())
    is_admin = graphene.Boolean(token=graphene.String())

    @staticmethod
    def resolve_is_admin(_, info, token=None):
        user = info.context.user
        return user.groups.filter(name='관리자').exists()

    @staticmethod
    def resolve_is_right_password(_, info, password):
        user = info.context.user
        return check_password(password, user.password)

    @staticmethod
    @login_required
    def resolve_me(_, info, **kwargs):
        return info.context.user


class Mutation(graphene.ObjectType):
    token_auth = ObtainJsonWebToken.Field()
    verify_token = VerifyToken.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    withdraw = Withdraw.Field()
    create_or_update_admin = CreateOrUpdateAdmin.Field()
    check_is_active = CheckIsActive.Field()
    check_is_parent = CheckIsParent.Field()
    change_password = ChangePassword.Field()
    set_fcm_token = SetFcmToken.Field()
    remove_fcm_token = RemoveFcmToken.Field()
    send_code = SendCode.Field()
    check_code = CheckCode.Field()
    set_password = SetPassword.Field()
    delete_token_cookie = graphql_jwt.DeleteJSONWebTokenCookie.Field()
    check_is_admin = CheckIsAdmin.Field()
    check_is_ta = CheckIsTa.Field()
    upload_profile_image = UploadProfileImage.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
