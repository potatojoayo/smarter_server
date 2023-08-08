from datetime import datetime

import graphene
import math

from order.models import OrderDetail, ZipCode
from payment.models import PaymentRequest
from server.settings import logger
from smarter_money.models import SmarterMoneyHistory


class CancelStudent(graphene.Mutation):
    class Arguments:
        order_detail_id = graphene.Int(required=True)
        student_name = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    @classmethod
    def mutate(cls, _, __, order_detail_id, student_name):
        try:
            old_order_detail = OrderDetail.objects.get(pk=order_detail_id)
            old_quantity = old_order_detail.quantity
            new_quantity = old_order_detail.quantity - 1
            product = old_order_detail.product
            gym = old_order_detail.order_master.user.gym
            if old_order_detail.state not in ['결제전', '결제완료', '무통장입금', '간편주문']:
                return CancelStudent(success=False, message="작업에 들어간 상품은 취소할수 없습니다.")
            extra_delivery = ZipCode.objects.filter(zip_code=old_order_detail.order_master.zip_code).first()
            if extra_delivery and extra_delivery.additional_delivery_price > 0 :
                extra_delivery_price = extra_delivery.additional_delivery_price
            else:
                extra_delivery_price = 0
            if old_order_detail.product.product_master.delivery_type == "분할배송상품":
                max_quantity_per_box = old_order_detail.product_master.max_quantity_per_box
                new_delivery_price_division = math.ceil(new_quantity/max_quantity_per_box)
                old_delivery_price_division = math.ceil(old_quantity/max_quantity_per_box)
                if old_delivery_price_division != new_delivery_price_division:
                    delivery_price = (old_delivery_price_division - new_delivery_price_division) * \
                                    (old_order_detail.product.product_master.price_delivery + extra_delivery_price)
                else:
                    delivery_price = 0
            elif old_order_detail.product.product_master.delivery_type == "개별배송상품":
                delivery_price = (old_order_detail.product_master.price_delivery + extra_delivery_price)
            else:
                delivery_price = 0

            price_work = old_order_detail.new_draft.price_work if old_order_detail.new_draft else 0
            price_option = product.price_additional
            price_products = product.product_master.price_gym
            if old_order_detail.state == "결제완료":
                user_wallet = gym.user.wallet
                user_wallet.balance += price_products + price_option + delivery_price
                user_wallet.save()
                old_cancel_student_order_detail = OrderDetail.objects.filter(
                    order_detail_number=old_order_detail.order_detail_number, student_names__isnull=False, state="주문취소")
                if old_cancel_student_order_detail.exists():
                    old_cancel_student_order_detail = old_cancel_student_order_detail.first()
                    old_cancel_student_order_detail.quantity += 1
                    old_cancel_student_order_detail.price_total = price_products + price_option
                    old_cancel_student_order_detail.student_names.append(student_name)
                    old_cancel_student_order_detail.save()
                else:
                    new_student_order_detail = OrderDetail.objects.create(order_master=old_order_detail.order_master,
                                                                          work=old_order_detail.work,
                                                                          order_detail_number=old_order_detail.order_detail_number,
                                                                          state="주문취소",
                                                                          product_master=old_order_detail.product_master,
                                                                          product=old_order_detail.product,
                                                                          quantity=1,
                                                                          price_total=price_products + price_option,
                                                                          price_products=price_products,
                                                                          price_work=old_order_detail.price_work,
                                                                          price_work_labor=old_order_detail.price_work_labor,
                                                                          price_option=old_order_detail.price_option,
                                                                          price_gym=old_order_detail.price_gym,
                                                                          price_consumer=old_order_detail.price_consumer,
                                                                          price_parent=old_order_detail.price_parent,
                                                                          price_vendor=old_order_detail.price_vendor)
                    new_student_order_detail.student_names.append(student_name)
                    new_student_order_detail.save()
                SmarterMoneyHistory.objects.create(order_master=old_order_detail.order_master,
                                                   history_number='H{}{}'.format(gym.user.phone,
                                                                                 datetime.now().strftime(
                                                                                     '%y%m%d%H%M%S')),
                                                   wallet=user_wallet,
                                                   amount=price_products + price_option,
                                                   description="{}제품 {}학생 삭제".format(old_order_detail.product.name,
                                                                                     student_name))
            else:
                payment_request = PaymentRequest.objects.filter(orderId=old_order_detail.order_master.order_number)
                if payment_request.count() > 0:
                    payment_request = payment_request.first()
                    payment_request.amount -= price_products + price_option + delivery_price
                    payment_request.save()
            gym.total_purchased_amount -= price_products + price_work - delivery_price
            old_order_detail.order_master.price_delivery -= delivery_price
            product.inventory_quantity += 1
            old_order_detail.quantity -= 1
            if old_order_detail.quantity == 0:
                old_order_detail.is_deleted = True
            old_order_detail.price_total -= price_products + price_option
            old_order_detail.student_names.remove(student_name)
            old_order_detail.save()
            product.save()
            old_order_detail.order_master.save()
            gym.save()
            return CancelStudent(success=True, message="완료되었습니다.")
        except Exception as e:
            logger.info('cancel_student_error')
            logger.info('order_detail_id : '+str(order_detail_id))
            logger.info('student_name : '+str(student_name))
            logger.info(e)
            return CancelStudent(success=False, message="알 수 없는 에러가 발생했습니다. 개발팀 문의 바랍니다.")