import math
from datetime import datetime

from smarter_money.models import SmarterMoneyHistory


def reward_smarter_money(order_master):
    user = order_master.user
    membership_percentage = user.gym.membership.percentage
    reward = math.floor(order_master.price_total_products * membership_percentage/100)
    user.wallet.balance += reward
    user.wallet.save()
    SmarterMoneyHistory.objects.create(
        order_master=order_master,
        history_number='R{}{}'.format(user.phone, datetime.now().strftime('%y%m%d%H%M%S')),
        wallet=user.wallet,
        transaction_type='적립',
        amount=reward,
        description=order_master.order_name
    )
