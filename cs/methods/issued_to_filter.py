from celery import shared_task
import re

from business.models import Gym
from cs.models import Coupon


@shared_task
def issued_to_filter(issued_to,  issued_price, coupon_master, start_of_use, end_of_use):
    if issued_to == "총 구매 금액":
        gyms = Gym.objects.filter(total_purchased_amount__gte=issued_price)
    else:
        gyms = Gym.objects.all()
    for gym in gyms:
        last_coupon = Coupon.objects.last()
        if last_coupon :
            last_coupon_number = last_coupon.coupon_number
            numbers = re.findall('\d+', last_coupon_number)
            only_number = int(numbers[0])
            coupon_number = 'C'+str(only_number+1)
        else:
            coupon_number = 'C00001'
        user = gym.user
        Coupon.objects.create(user=user,
                              coupon_master=coupon_master,
                              coupon_number=coupon_number,
                              price=coupon_master.price,
                              start_of_use=start_of_use,
                              end_of_use=end_of_use
                              )


