from celery import shared_task

from authentication.models import User
from business.models import Gym
from common.methods.send_notification import send_notification
from cs.models import CouponMaster, Coupon, CouponIssueHistory
from datetime import datetime, timedelta

@shared_task
def issue_referral_coupon(referral_user_id, nominee_id):
    referral_user = User.objects.get(pk=referral_user_id)
    nominee_gym = Gym.objects.get(pk=nominee_id)
    referral_coupon_master = CouponMaster.objects.get(name="추천인쿠폰")
    referral_coupon_number = referral_coupon_master.count_per_issue
    now = datetime.now()
    for i in range(referral_coupon_number):
        coupon_number = 'CR' + str(now.year)[2:4] + \
                        str(now.month).rjust(2, '0') + \
                        str(now.day).rjust(2, '0') + \
                        str(now.hour).rjust(2, '0') + \
                        str(now.minute).rjust(2, '0') + \
                        str(now.second).rjust(2, '0') + \
                        str(referral_user.id % 100).rjust(2, '0') + str(i + 1)
        start_of_use = now
        end_of_use = now + timedelta(days=referral_coupon_master.expire_day)
        coupon = Coupon.objects.create(user=referral_user, coupon_master=referral_coupon_master,
                              coupon_number=coupon_number, price=referral_coupon_master.price,
                              start_of_use=start_of_use, end_of_use=end_of_use, nominee=nominee_gym,
                              referral_code=referral_user.phone)
        CouponIssueHistory.objects.create(coupon=coupon, gym=referral_user.gym, coupon_number=coupon_number, gym_name=referral_user.gym.name,
                                          price=coupon.price, start_of_use=coupon.start_of_use, end_of_use=coupon.end_of_use)
    send_notification(user=referral_user, type="쿠폰발급", coupon_master=referral_coupon_master)