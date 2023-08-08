from django.db import transaction
from django.utils import timezone
import graphene
from cs.methods.get_order_state import get_order_state
from cs.models import CsRequest, CancelOrderRequest
from smarter_money.models import SmarterMoneyHistory


class CsCancelOrder(graphene.Mutation):
    class Arguments:
        cs_request_id = graphene.Int(required=True)

    success = graphene.Boolean(default_value=False)
    message = graphene.String()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, cs_request_id):
        try:
            cs_request = CsRequest.objects.get(pk=cs_request_id)
            order_master = cs_request.order_master
            order_state = get_order_state(order_master)
            if order_state not in ['결제전', '결제완료']:
                return CsCancelOrder(success=False, message='작업 또는 배송에 들어간 상품이 있을 경우 주문 취소가 불가능합니다.')

            order_master.details.all().update(state='주문취소')

            if order_state == '결제완료':
                user = order_master.user
                paid_amount = order_master.price_to_pay
                user.wallet.balance += paid_amount
                user.wallet.save()
                SmarterMoneyHistory.objects.create(
                    history_number='H{}{}'.format(user.phone, timezone.now().strftime('%y%m%d%H%M%S')),
                    wallet=user.wallet,
                    transaction_type="환불",
                    amount=paid_amount,
                    order_number=order_master.order_number,
                    order_master=order_master,
                    description='{} 주문 취소'.format(order_master.order_name)
                )

            CancelOrderRequest.objects.create(cs_request=cs_request,
                                              cs_request_number=cs_request.request_number,
                                              order_master=order_master,
                                              order_number=order_master.order_number,
                                              gym_name=order_master.user.gym.name,
                                              reason=cs_request.reason,
                                              price_products=order_master.price_total_products,
                                              price_works=order_master.price_total_work,
                                              price_delivery=order_master.price_delivery,
                                              price_total=order_master.price_to_pay,
                                              state='취소완료',
                                              date_completed=timezone.now()
                                              )
            cs_request.order_state = '주문취소'
            cs_request.save()

            return CsCancelOrder(success=True, message='주문이 취소되었습니다.')
        except Exception as e:
            import logging
            logger = logging.getLogger('myLog')
            logger.info(e)
            return CsCancelOrder(success=False)
