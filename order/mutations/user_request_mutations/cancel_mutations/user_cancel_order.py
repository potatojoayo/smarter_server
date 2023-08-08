from datetime import datetime

import graphene
from django.db import transaction

from cs.methods.get_order_state import get_order_state
from cs.models import CsRequest, CancelOrderRequest, CsRequestContents
from inventory.models import ChangeHistory
from order.models import OrderMaster
from payment.models import PaymentSuccess
from product.models import Product
from smarter_money.models import SmarterMoneyHistory


class UserCancelOrder(graphene.Mutation):
    class Arguments:
        order_master_id = graphene.Int(required=True)

    success = graphene.Boolean(required=True)
    message = graphene.String(required=True)

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, info, order_master_id):
        try:
            order_master = OrderMaster.objects.get(pk=order_master_id)
            payment_success = PaymentSuccess.objects.filter(orderId=order_master.order_number)
            is_paid = payment_success.count() > 0
            user = order_master.user
            gym = user.gym
            order_state = get_order_state(order_master)
            if order_state == '주문취소':
                return UserCancelOrder(success=False, message='이미 취소된 주문입니다.')
            if order_state not in ['결제전', '결제완료']:
                return UserCancelOrder(success=False, message='작업 또는 배송에 들어간 상품이 있을 경우 주문 취소가 불가능합니다.')

            now = datetime.now()

            products = {}
            order_details = order_master.details.all()

            state = '취소완료'
            cs_state = '미처리'
            cs_request = None
            is_without_deposit = False
            for order_detail in order_details:
                if is_paid:
                    for payment in payment_success:
                        if payment.method == '스마터머니':
                            SmarterMoneyHistory.objects.create(
                                order_master=order_master,
                                history_number='R{}{}'.format(user.phone, datetime.now().strftime('%y%m%d%H%M%S')),
                                wallet=user.wallet,
                                transaction_type='환불',
                                amount=payment.amount,
                                description='스마터머니 결제 주문 취소')
                            user.wallet.balance += payment.amount
                            user.wallet.save()

                        # 무통장 입금 완료
                        if payment.method == "무통장입금":
                            order_detail.state = "취소요청"
                            order_detail.save()
                            is_without_deposit = True

                            request_number = 'R' + str(now.year)[2:4] + \
                                             str(now.month).rjust(2, '0') + \
                                             str(now.day).rjust(2, '0') + \
                                             str(now.hour).rjust(2, '0') + \
                                             str(now.minute).rjust(2, '0') + \
                                             str(now.second).rjust(2, '0') + \
                                             str(gym.id % 100).rjust(2, '0')

                            state = '취소요청'
                            cs_request = CsRequest.objects.create(gym=gym,
                                                                  order_master=order_master,
                                                                  request_number=request_number,
                                                                  category="무통장입금취소",
                                                                  cs_state=cs_state,
                                                                  order_number=order_master.order_number,
                                                                  order_state=order_state,
                                                                  reason='단순변심')

                            cs_request.request_contents.add(CsRequestContents.objects.create(
                                cs_request=cs_request,
                                contents='앱에서 무통장입금 취소 요청'),
                            )

                        # 무통장 입금 전
                        else:
                            order_detail.state = "취소완료"
                            order_detail.save()
                            product_id = str(order_detail.product_id)
                            if product_id in products:
                                products[product_id]['quantity'] += order_detail.quantity
                            else:
                                products[product_id] = {
                                    'quantity': order_detail.quantity, 'order_detail': order_detail
                                }

                else:
                    order_detail.state = "취소완료"
                    order_detail.save()


                if not is_without_deposit:
                    product_id = str(order_detail.product_id)
                    if product_id in products:
                        products[product_id]['quantity'] += order_detail.quantity
                    else:
                        products[product_id] = {
                            'quantity': order_detail.quantity, 'order_detail': order_detail
                        }


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

            CancelOrderRequest.objects.create(cs_request=cs_request,
                                              cs_request_number=cs_request.request_number if cs_request else None,
                                              order_master=order_master,
                                              order_number=order_master.order_number,
                                              is_without_deposit=is_without_deposit,
                                              gym_name=gym.name,
                                              reason='단순변심',
                                              price_products=order_master.price_total_products,
                                              price_works=order_master.price_total_work,
                                              price_delivery=order_master.price_delivery,
                                              price_total=order_master.price_to_pay,
                                              state=state
                                              )

            return UserCancelOrder(success=True, message='주문이 취소되었습니다.')
        except Exception as e:
            print(e)
            return UserCancelOrder(success=False, message='주문 취소에 실패하였습니다. 고객센터에 문의해주세요.')




