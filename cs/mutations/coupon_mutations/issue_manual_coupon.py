import graphene
from django.db import transaction

from business.models import Gym
from cs.methods.coupon_methods.issue_coupon import issue_coupon
from cs.models import Coupon, CouponMaster, CouponMasterIssueHistory
from datetime import datetime, timedelta


class IssueManualCoupon(graphene.Mutation):
    class Arguments:
        coupon_master_id = graphene.Int(required=True)
        gym_ids = graphene.List(graphene.Int, required=True)
        issue_number = graphene.Int(required=True)
        expire_day = graphene.Int(required=True)
        coupon_message = graphene.String(required=True)
        search_type = graphene.String()
        address_zip_code_id = graphene.Int()
        condition = graphene.String()
        threshold_amount = graphene.Int()

    success = graphene.Boolean()
    message = graphene.String()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, coupon_master_id, gym_ids, expire_day, issue_number, coupon_message, search_type, address_zip_code_id=None, condition=None, threshold_amount=None):
        try:
            coupon_master = CouponMaster.objects.get(pk=coupon_master_id)
            price = coupon_master.price
            now = datetime.now()
            start_of_use = now
            end_of_use = now + timedelta(days=expire_day)
            history = CouponMasterIssueHistory.objects.create(
                coupon_master=coupon_master,
                issued_address_id=address_zip_code_id,
                condition=condition, threshold_amount=threshold_amount,
                issued_count_per_gym=issue_number,
                issued_amount_per_gym=issue_number * coupon_master.price,
                total_issued_count=issue_number * len(gym_ids),
                total_issued_amount=issue_number * len(gym_ids) * coupon_master.price,
                coupon_message=coupon_message,
                expired_day=expire_day,
                search_type=search_type
            )
            for gym_id in gym_ids:
                gym = Gym.objects.get(pk=gym_id)
                history.issued_gyms.add(gym)
                user = gym.user
                issue_coupon.delay(coupon_master_name=coupon_master.name, user_id=user.id, issue_number=issue_number,
                                   start_of_use=start_of_use, end_of_use=end_of_use, coupon_message=coupon_message)
            history.save()
            return IssueManualCoupon(success=True, message='{} 쿠폰이 성공적으로 발급되었습니다.'.format(coupon_master.name))
        except Exception as e:
            print(e)
            import logging
            logger = logging.getLogger('myLog')
            logger.info(e)
            return IssueManualCoupon(success=False, message='쿠폰 발급이 실패하였습니다. 개발팀에게 문의해주세요.')
