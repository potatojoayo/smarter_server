import graphene

from authentication.models import User


class SetPassword(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int()
        new_password = graphene.String()
        confirm_password = graphene.String()

    success = graphene.Boolean()
    message = graphene.String()
    @classmethod
    def mutate(cls, _, __, user_id, new_password, confirm_password):
        if new_password != confirm_password:
            return SetPassword(success=False, message ="비밀번호와 비밀번호 확인 번호가 일치하지않습니다. 정확하게 입력해주십길 바랍니다.")
        try:
            user = User.objects.get(pk=user_id)
            user.set_password(new_password)
            user.save()
            return SetPassword(success=True, message = "비밀번호가 성공적으로 변경되었습니다. 재로그인 부탁드립니다.")
        except User.DoesNotExist:
            return SetPassword(success=False, message="비밀번호 변경에 실패하였습니다. 재시도 부탁드립니다.")
