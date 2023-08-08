import graphene
from django.db import transaction

from cs.methods.get_order_state import get_order_state
from cs.models import CsPartialCancelHistory, CancelOrderRequest
from inventory.models import ChangeHistory
from product.models import Product
from smarter_money.models import SmarterMoneyHistory
from datetime import datetime

class ConcludeCancelOrderWithoutDeposit(graphene.Mutation):
    class Arguments:
        cancel_ids = graphene.List(graphene.Int)

    success = graphene.Boolean()
    message = graphene.String()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, cancel_ids):
        try:
            cancel_order_requests = CancelOrderRequest.objects.filter(pk__in=cancel_ids)
            ## 결제전, 결제완료 아닌 리스트들 분리, 아닌것들은 취소 처리 안해주고 인것들은 처리, return 값에 취소불가인 request들 표시해줌
            states = list(set([cancel_order_request.state for cancel_order_request in cancel_order_requests]))
            if '취소완료' in states:
                return ConcludeCancelOrderWithoutDeposit(success=False, message="취소요청 상태들만 처리가 가능합니다.")
            not_proceed_cancel_order_list = []
            proceed_cancel_order_list = []
            for cancel_order_request in cancel_order_requests:
                order_state = get_order_state(cancel_order_request.order_master)
                if order_state not in['결제전', '결제완료']:
                    not_proceed_cancel_order_list.append(cancel_order_request)
                else:
                    proceed_cancel_order_list.append(cancel_order_request)

            for cancel_order_request in proceed_cancel_order_list:
                products = {}
                for order_detail in cancel_order_request.order_master.details.all():
                    product_id = str(order_detail.product_id)
                    order_detail.state = '취소완료'
                    order_detail.save()
                    if product_id in products:
                        products[product_id]['quantity'] += order_detail.quantity
                    else:
                        products[product_id] = {
                            'quantity': order_detail.quantity, 'order_detail': order_detail
                        }
                cancel_order_request.state = '취소완료'
                cancel_order_request.save()

                for key, value in products.items():
                    quantity = value['quantity']
                    order_detail = value['order_detail']
                    product = Product.objects.get(pk=int(key))
                    quantity_before = product.inventory_quantity
                    quantity_after = product.inventory_quantity + quantity
                    quantity_changed = quantity
                    product_master = product.product_master
                    gym = order_detail.order_master.user.gym
                    gym.total_purchased_amount -= order_detail.price_gym * order_detail.quantity + order_detail.price_work
                    gym.save()
                    if quantity_after <= 0:
                        lack_inventory = True
                    else:
                        lack_inventory = False
                    Product.objects.filter(pk=int(key)).update(inventory_quantity=quantity_after, lack_inventory=lack_inventory)
                    ChangeHistory.objects.create(order_detail=order_detail, product_master=product_master, product=product,
                                                 quantity_before=quantity_before,
                                                 quantity_after=quantity_after, quantity_changed=quantity_changed, reason='취소')

            return ConcludeCancelOrderWithoutDeposit(success=True, message='선택하신 취소요청들이 완료되었습니다.')

        except Exception as e:
            import logging
            logger = logging.getLogger('myLog')
            logger.info(e)
            return ConcludeCancelOrderWithoutDeposit(success=False, message='알 수 없는 에러가 발생했습니다. 개발팀 문의 바랍니다.')







