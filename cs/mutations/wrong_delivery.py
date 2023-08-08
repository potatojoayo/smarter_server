from datetime import datetime

import graphene

from order.models import OrderDetail, OrderMaster
from server.settings import logger
from smarter_money.models import SmarterMoneyHistory, SmarterPaidHistory


class WrongDelivery(graphene.Mutation):
    class Arguments:
        order_master_id = graphene.Int()
        order_detail_ids = graphene.List(graphene.Int)

    success = graphene.Boolean()
    message = graphene.String()

    @classmethod
    def mutate(cls, _, __, order_master_id, order_detail_ids):
        try:
            order_master = OrderMaster.objects.get(pk=order_master_id)
            order_details = OrderDetail.objects.filter(pk__in=order_detail_ids)
            total_return_price = order_master.price_delivery
            for order_detail in order_details:
                order_detail.state = "오배송"
                total_return_price += order_detail.price_total
                order_detail.save()

            user = order_master.user
            user_wallet = user.wallet
            user_wallet.balance += total_return_price
            SmarterMoneyHistory.objects.create(
                history_number='R{}{}'.format(user.phone, datetime.now().strftime('%y%m%d%H%M%S')),
                wallet = user_wallet,
                order_master=order_master,
                order_number=order_master.order_number,
                transaction_type="적립",
                description="오배송으로 인한 스마터머니 적립",
                amount=total_return_price
            )
            smarter_paid_history = SmarterPaidHistory.objects.create(amount=total_return_price, reason="오배송")
            smarter_paid_history.order_details.add(*order_details)

            return WrongDelivery(success=True, message="오배송 환불처리가 완료되었습니다.")
        except Exception as e:
            logger.info(e)
            return WrongDelivery(success=False, message="오류가 발생하였습니다. 개발팀에 문의해주세요.")



