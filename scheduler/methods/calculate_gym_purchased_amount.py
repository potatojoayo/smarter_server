from datetime import datetime

from business.models import Gym, GymMonthlyPurchasedAmount
from payment.models import PaymentSuccess
from server.celery import app, logger


@app.task
def calculate_gym_purchased_amount():
    logger.info('calculate_gym_purchased_amount start')
    now = datetime.now()
    year = now.year
    month = now.month
    logger.info('now : '+str(now))
    logger.info('year : '+str(year))
    logger.info('month : '+str(month))
    gyms = Gym.objects.all()
    for gym in gyms:
        user = gym.user
        order_masters = user.orders.filter(date_created__gte=datetime(year=year, month=month-1, day=1),
                                           date_created__lt=datetime(year=year, month=month, day=1))
        if order_masters.exists():
            for order_master in order_masters:
                payment_successes = PaymentSuccess.objects.filter(orderId=order_master.order_number)
                if payment_successes.exists():
                    payment_success = payment_successes.first()
                    gym.total_purchased_amount += payment_success.amount
                    logger.info('{} total_purchased_amount {}원추가 => {}원'.format(gym.name, payment_success.amount, gym.total_purchased_amount))
                    monthly_purchased_amount , created = GymMonthlyPurchasedAmount.objects.get_or_create(gym=gym, date=datetime(year=year, month=month, day=1).date())
                    if created:
                        logger.info('{} {}년 {}월 GymMonthlyPurchasedAmount 생성'.format(gym.name, year, month))
                    monthly_purchased_amount.amount +=payment_success.amount
                    monthly_purchased_amount.save()
        gym.save()

