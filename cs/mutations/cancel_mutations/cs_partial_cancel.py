from datetime import datetime
import graphene
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from cs.methods.get_order_state_detail import get_order_state_detail
from cs.methods.delivery_methods.new_price_delivery_method import new_price_delivery_method
from cs.models import CsRequest, CsPartialCancelHistory
from order.models import OrderDetail
from payment.models import PaymentRequest
from smarter_money.models import SmarterMoneyHistory


class CsPartialCancel(graphene.Mutation):
    class Arguments:
        cs_request_id = graphene.Int()
        order_detail_ids = graphene.List(graphene.Int)

    success = graphene.Boolean()
    message = graphene.String()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, cs_request_id,  order_detail_ids):
        try:
            cs_request = CsRequest.objects.get(pk=cs_request_id)
            order_master = cs_request.order_master
            order_details = OrderDetail.objects.filter(pk__in=order_detail_ids)
            order_state = get_order_state_detail(order_details=order_details)
            total_price = 0
            if order_state not in ['결제전', '결제완료']:
                return CsPartialCancel(success=False, message='작업 또는 배송에 들어간 상품이 있을 경우 주문 변경이 불가능합니다.')
            for order_detail in order_details:
                order_detail.is_deleted = True
                order_detail.state = "부분취소"
                total_price += order_detail.price_total
                CsPartialCancelHistory.objects.create(cs_request=cs_request,
                                                      order_master=order_master,
                                                      order_detail=order_detail,
                                                      cs_request_number=cs_request.request_number,
                                                      order_number=order_master.order_number,
                                                      product_name=order_detail.product_master.name,
                                                      gym_name=cs_request.gym.name,
                                                      reason=cs_request.reason,
                                                      color=order_detail.product.color,
                                                      size=order_detail.product.size,
                                                      price_product=order_detail.product.price_additional+ order_detail.product_master.price_gym,
                                                      price_total=order_detail.price_total,
                                                      canceled_quantity=order_detail.quantity,
                                                      description='주문 부분취소'
                                                      )
                order_detail.save()
            order_master.save()
            new_delivery_price = new_price_delivery_method(order_master)
            price_delivery_difference = order_master.price_delivery - new_delivery_price
            order_master.price_delivery = new_delivery_price
            order_master.save()
            gym = cs_request.gym
            user = gym.user
            if order_state == "결제전":
                gym.total_purchased_amount -= total_price
                try:
                    payment_request = PaymentRequest.objects.get(orderId=order_master.order_number)
                    new_payment_amount = order_master.price_total + order_master.price_delivery
                    payment_request.amount = new_payment_amount
                    payment_request.save()
                except ObjectDoesNotExist:
                    pass
            else:
                user_wallet = user.wallet
                user_wallet.balance += total_price + price_delivery_difference
                user_wallet.save()
                SmarterMoneyHistory.objects.create(order_master=order_master,
                                                   history_number='H{}{}'.format(user.phone, datetime.now().strftime(
                                                       '%y%m%d%H%M%S')),
                                                   wallet=user_wallet,
                                                   transaction_type="적립",
                                                   amount=total_price + price_delivery_difference,
                                                   description="주문 부분취소로 인한 스마터머니 적립")
            return CsPartialCancel(success=True, message="주문 부분취소가 완료되었습니다.")
        except Exception as e:
            print(e)
            import logging
            logger = logging.getLogger('myLog')
            logger.info(e)
            return CsPartialCancel(success=False, message="알수없는 오류가 발생하였습니다. 개발팀에 문의해주세요.")

