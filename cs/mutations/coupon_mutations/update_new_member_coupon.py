import graphene

from cs.models import CouponMaster
from cs.types.coupon_types.coupon_master_type import CouponMasterType


class UpdateNewMemberCoupon(graphene.Mutation):
    class Arguments:
        price = graphene.Int()
        count_per_issue = graphene.Int()
        expire_day = graphene.Int()

    success = graphene.Boolean()
    coupon_master = graphene.Field(CouponMasterType)

    @classmethod
    def mutate(cls, _, __, price, count_per_issue, expire_day):
        try:
            new_member_coupon = CouponMaster.objects.get(name="신규가입쿠폰")
            new_member_coupon.price = price
            new_member_coupon.count_per_issue = count_per_issue
            new_member_coupon.expire_day = expire_day
            new_member_coupon.save()

            return UpdateNewMemberCoupon(success=True, coupon_master=new_member_coupon)
        except Exception as e:
            import logging
            logger = logging.getLogger('myLog')
            logger.info(e)
            return UpdateNewMemberCoupon(success=False)




