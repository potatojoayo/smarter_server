from datetime import datetime

from django.db.models import IntegerField, Func, Sum, F, Value
from django.db.models.functions import Cast

from authentication.models import User
from business.models import Gym
import graphene

from cs.models import Coupon, CouponMaster

ko_kr = Func(
    "owner_name",
    function="ko_KR.utf8",
    template='(%(expressions)s) COLLATE "%(function)s"'
)

class TestNumber(graphene.Mutation):
    class Arguments:
        number1 = graphene.Int()
        number2 = graphene.Int()


    number = graphene.String()

    @classmethod
    def mutate(cls, _, info, **kwargs):

        total = CouponMaster.objects.aggregate(total=Sum('expire_day'))['total']
        print(total)
        coupon_masters = CouponMaster.objects.annotate(amounts=Value(total))
        for coupon_master in coupon_masters:
            print(coupon_master.name)
            print(coupon_master.amounts)
        return TestNumber(number='0')