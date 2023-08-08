import datetime, time
import json
import graphene
from django.core.exceptions import ObjectDoesNotExist

from authentication.methods.solapi_async_message import solapi_async_message
from authentication.models import User
from src.lib import message
import random

class SendCode(graphene.Mutation):
    class Arguments:
        identification = graphene.String()
        phone_number = graphene.String()

    success = graphene.Boolean()
    message = graphene.String()
    @classmethod
    def mutate(cls, _, __, identification, phone_number):
        try:
            print(identification)
            print(phone_number)
            user = User.objects.get(identification=identification,
                                    phone=phone_number)
            random_int = random.randint(100000, 999999)

            solapi_async_message.delay(phone_number=phone_number, random_int=random_int)
            # res = message.send_many(data)
            # print(json.dumps(res.json(), indent=2, ensure_ascii=False))
            user.code_for_password = random_int
            user.code_limit_time = datetime.datetime.now() + datetime.timedelta(minutes=5, seconds=1)
            user.save()
            return SendCode(success=True, message="인증번호를 보냈습니다")
        except ObjectDoesNotExist:
            return SendCode(success=False, message="일치하는정보가 없습니다")






