import graphene

from cs.models import CouponMaster
from cs.types.coupon_types.coupon_master_type import CouponMasterType


class UpdateReferralCoupon(graphene.Mutation):
    class Arguments:

        price = graphene.Int()
        count_per_issue = graphene.Int()
        expire_day = graphene.Int()

    success= graphene.Boolean()
    coupon_master = graphene.Field(CouponMasterType)
    @classmethod
    def mutate(cls, _, __, price, count_per_issue, expire_day):
        try:
            referral_coupon = CouponMaster.objects.get(name="추천인쿠폰")
            referral_coupon.price = price
            referral_coupon.count_per_issue = count_per_issue
            referral_coupon.expire_day = expire_day
            referral_coupon.save()

            return UpdateReferralCoupon(success=True, coupon_master=referral_coupon)
        except Exception as e:
            import logging
            logger = logging.getLogger('myLog')
            logger.info(e)
            return UpdateReferralCoupon(success=False)




