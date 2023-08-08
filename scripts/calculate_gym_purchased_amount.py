from django.db import transaction
from datetime import datetime

from business.models import Gym, GymMonthlyPurchasedAmount
from payment.models import PaymentSuccess


@transaction.atomic()
def run():
    gyms = Gym.objects.all()
    for gym in gyms:
        user = gym.user
        order_masters = user.orders.all()
        for order_master in order_masters:
            payment_successes = PaymentSuccess.objects.filter(orderId=order_master.order_number)
            if payment_successes.exists():
                payment_success = payment_successes.first()
                gym.total_purchased_amount += payment_success.amount
                print('{} total_purchased_amount {}원 추가 => {}원'.format(gym.name, payment_success.amount, gym.total_purchased_amount))
                year = payment_success.requestedAt.year
                month = payment_success.requestedAt.month
                date = datetime(year=year, month=month, day=1)
                monthly_purchased_amount, created = GymMonthlyPurchasedAmount.objects.get_or_create(gym=gym, date=date)
                if created:
                    print('{} {}년 {}월 GymMonthlyPurchasedAmount 생성'.format(gym.name, year, month))
                monthly_purchased_amount.amount += payment_success.amount
                monthly_purchased_amount.save()

        gym.save()




