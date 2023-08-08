from cs.models import CouponMaster, Coupon, CouponIssueHistory
from datetime import datetime, timedelta

def issue_new_coupon(user):
    new_coupon_master = CouponMaster.objects.get(name="신규가입쿠폰")
    new_coupon_number = new_coupon_master.count_per_issue
    now = datetime.now()
    gym_id = user.gym.id
    for i in range(new_coupon_number):
        coupon_number = 'CN' + str(now.year)[2:4] + \
                        str(now.month).rjust(2, '0') + \
                        str(now.day).rjust(2, '0') + \
                        str(now.hour).rjust(2, '0') + \
                        str(now.minute).rjust(2, '0') + \
                        str(now.second).rjust(2, '0') + \
                        str(gym_id % 100).rjust(2, '0') + str(i + 1)
        start_of_use = now
        end_of_use = now + timedelta(days=new_coupon_master.expire_day)

        Coupon.objects.create(user=user, coupon_master=new_coupon_master, coupon_number=coupon_number,
                                       price=new_coupon_master.price, start_of_use=start_of_use,
                                       end_of_use=end_of_use )
