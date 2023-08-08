import graphene
import math
from django.db import transaction
from datetime import datetime
from cs.methods.get_order_state_detail import get_order_state_detail
from cs.models import CsRequest
from cs.models.cs_partial_cancel_history import CsPartialCancelHistory
from order.models import OrderDetail, ZipCode
from payment.models import PaymentRequest
from smarter_money.models import SmarterMoneyHistory


class ChangeOrderDetailQuantity(graphene.Mutation):
    class Arguments:
        cs_request_id = graphene.Int()
        order_detail_id = graphene.Int()
        new_quantity = graphene.Int()

    success = graphene.Boolean()
    message = graphene.String()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, order_detail_id, new_quantity, cs_request_id):
        try:
            cs_request = CsRequest.objects.get(pk=cs_request_id)
            order_detail = OrderDetail.objects.filter(pk=order_detail_id)
            user = cs_request.gym.user
            gym = cs_request.gym
            order_state = get_order_state_detail(order_details=order_detail)
            order_detail = order_detail.first()
            product = order_detail.product
            if order_state not in ['결제전', '결제완료']:
                return ChangeOrderDetailQuantity(success=False, message='작업 또는 배송에 들어간 상품이 있을 경우 주문 변경이 불가능합니다.')
            old_order_detail_quantity = order_detail.quantity
            if old_order_detail_quantity < new_quantity:
                return ChangeOrderDetailQuantity(success=False,
                                                 message='수정하려는 제품의 수량이 이전 수량보다 많습니다. 추가주문을 해주세요')
            if old_order_detail_quantity == new_quantity:
                return ChangeOrderDetailQuantity(success=False,
                                                 message='수정하려는 제품의 수량이 동일합니다')
            extra_delivery = ZipCode.objects.filter(zip_code=order_detail.order_master.zip_code).first()
            if extra_delivery and extra_delivery.additional_delivery_price > 0:
                extra_delivery_price = extra_delivery.additional_delivery_price
            else:
                extra_delivery_price = 0
            # order_details_num = order_detail.order_master.details.filter(is_deleted=False).count()
            product_number_difference = old_order_detail_quantity - new_quantity
            ## delivery price : 빠지는 배송비값
            if order_detail.product.product_master.delivery_type == "분할배송상품":
                max_quantity_per_box = order_detail.product_master.max_quantity_per_box
                new_delivery_price_division = math.ceil(new_quantity / max_quantity_per_box)
                old_delivery_price_division = math.ceil(old_order_detail_quantity / max_quantity_per_box)
                if old_delivery_price_division != new_delivery_price_division:
                    delivery_price = (old_delivery_price_division - new_delivery_price_division) * \
                                     (order_detail.product.product_master.price_delivery + extra_delivery_price)
                else:
                    delivery_price = order_detail.product.product_master.price_delivery
            elif order_detail.product.product_master.delivery_type == "개별배송상품":
                delivery_price = (order_detail.product.product_master.price_delivery + extra_delivery_price) * product_number_difference
            else:
                delivery_price = order_detail.product.product_master.price_delivery
            # 이전 order_detail의 가격과 지금 order_detail의 가격 차이
            price_difference = order_detail.price_total - (order_detail.product_master.price_gym * new_quantity)
            if order_state == "결제전":
                if order_detail.new_draft:
                    price_work = order_detail.new_draft.price_work * new_quantity
                    price_work_labor = order_detail.new_draft.price_work_labor * new_quantity
                else:
                    price_work = 0
                    price_work_labor = 0
                price_option = product.price_additional * new_quantity
                price_products = product.product_master.price_gym * new_quantity
                gym.total_purchased_amount -= order_detail.price_gym * new_quantity + price_work - delivery_price
                order_detail.order_master.price_delivery -= delivery_price
                payment_request = PaymentRequest.objects.filter(orderId=order_detail.order_master.order_number)
                # 새로운 수량를 적용해 order_detail의 총 가격을 적용해줌
                order_detail.quantity = new_quantity
                order_detail.price_total = price_products + price_work + price_work_labor
                order_detail.price_option = price_option
                order_detail.price_products = price_products
                order_detail.price_work = price_work
                order_detail.price_work_labor = price_work_labor
                order_detail.is_changed = True
                if payment_request.count() > 0:
                    payment_request = payment_request.first()
                    payment_request.amount -= price_difference + delivery_price
                    payment_request.save()
                product.inventory_quantity += old_order_detail_quantity - new_quantity
                product.save()
                ## 카톡 메세지 알람 보내줘야하는지??
            else:
                user_wallet = user.wallet
                user_wallet.balance += price_difference + delivery_price
                user_wallet.save()
                order_detail.quantity = new_quantity
                price_work = order_detail.new_draft.price_work if order_detail.new_draft else 0
                order_detail.price_total = (order_detail.product_master.price_gym+price_work) * new_quantity
                order_detail.save()
                cancel_order_detail = order_detail
                cancel_order_detail.pk = None
                cancel_order_detail.state = "주문취소"
                cancel_order_detail.quantity = product_number_difference
                cancel_order_detail.price_total = (cancel_order_detail.product_master.price_gym+price_work) * product_number_difference
                cancel_order_detail.save()

                SmarterMoneyHistory.objects.create(order_master=order_detail.order_master,
                                                   history_number='H{}{}'.format(user.phone, datetime.now().strftime(
                                                       '%y%m%d%H%M%S')),
                                                   wallet=user_wallet,
                                                   transaction_type="환불",
                                                   amount=price_difference,
                                                   description=order_detail.product.name + " 주문수량 차감으로 인한 스마터머니 환불")
            order_detail.save()
            order_detail.order_master.save()
            gym.save()
            CsPartialCancelHistory.objects.create(cs_request=cs_request,
                                                  order_master=order_detail.order_master,
                                                  order_detail=order_detail,
                                                  description="주문수량 변경",
                                                  cs_request_number=cs_request.request_number,
                                                  order_number=order_detail.order_master.order_number,
                                                  product_name=order_detail.product.name,
                                                  gym_name=gym.name,
                                                  reason=cs_request.reason,
                                                  color=order_detail.product.color,
                                                  size=order_detail.product.size,
                                                  price_product=order_detail.product_master.price_gym + order_detail.product.price_additional,
                                                  canceled_quantity=product_number_difference,
                                                  price_total=(order_detail.product_master.price_gym + order_detail.product.price_additional)*product_number_difference
                                                  )
            return ChangeOrderDetailQuantity(success=True, message="주문수량이 변경되었습니다.")
        except Exception as e:
            import logging
            logger = logging.getLogger('myLog')
            logger.info(e)
            return ChangeOrderDetailQuantity(success=False, message='알 수 없는 에러가 발생했습니다. 개발팀 문의 바랍니다.')
