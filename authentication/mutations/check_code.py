from datetime import datetime

import pytz
from django.utils import timezone
import graphene

from authentication.models import User


class CheckCode(graphene.Mutation):
    class Arguments:
        code = graphene.Int()
        identification = graphene.String()
        phone_number = graphene.String()

    success = graphene.Boolean()
    user_id = graphene.Int()
    message = graphene.String()

    @classmethod
    def mutate(cls, _, __, code, identification, phone_number):
        timezone_seoul = pytz.timezone('Asia/Seoul')
        now_time = datetime.now()
        now = timezone_seoul.localize(now_time)
        user = User.objects.get(identification=identification,
                                phone=phone_number)
        if user.code_for_password == code and user.code_limit_time > now :
            return CheckCode(success=True, user_id = user.id, message = "인증번호가 성공적으로 입력되었습니다.")
        elif user.code_for_password != code:
            return CheckCode(success=False, user_id = None, message = "인증번호가 틀렸습니다.")
        elif user.code_limit_time < now :
            return CheckCode(success=False, user_id = None, message = "인증번호 유효시간이 지났습니다. 인증번호 재발급 부탁드립니다.")