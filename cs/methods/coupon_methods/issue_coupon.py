from datetime import datetime, timedelta

from celery import shared_task

from authentication.models import User
from common.methods.send_notification import send_notification
from cs.models import CouponMaster, Coupon, CouponIssueHistory

@shared_task
def issue_coupon(coupon_master_name, user_id, issue_number=None, start_of_use=None, end_of_use=None, coupon_message=None):
    coupon_master = CouponMaster.objects.get(name=coupon_master_name)
    issue_coupon_number = coupon_master.count_per_issue if coupon_master.count_per_issue else issue_number
    now = datetime.now()
    user = User.objects.get(pk=user_id)
    gym = user.gym
    gym_id = gym.id
    for i in range(issue_coupon_number):
        coupon_number = 'CN' + str(now.year)[2:4] + \
                        str(now.month).rjust(2, '0') + \
                        str(now.day).rjust(2, '0') + \
                        str(now.hour).rjust(2, '0') + \
                        str(now.minute).rjust(2, '0') + \
                        str(now.second).rjust(2, '0') + \
                        str(gym_id % 100).rjust(2, '0') + str(i + 1)
        start_of_use = now if coupon_master.expire_day else start_of_use
        end_of_use = now + timedelta(days=coupon_master.expire_day) if coupon_master.expire_day else end_of_use
        coupon = Coupon.objects.create(user=user, coupon_master=coupon_master, coupon_number=coupon_number,
                                       price=coupon_master.price, start_of_use=start_of_use,
                                       end_of_use=end_of_use )
        CouponIssueHistory.objects.create(coupon=coupon, gym=gym, coupon_number=coupon_number, gym_name=gym.name,
                                          price=coupon.price, start_of_use=coupon.start_of_use, end_of_use=coupon.end_of_use)
    send_notification(user=user, type="쿠폰발급",coupon_master=coupon_master, issue_coupon_number=issue_coupon_number, coupon_message=coupon_message)
