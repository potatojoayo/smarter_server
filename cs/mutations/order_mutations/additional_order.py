from datetime import datetime

import graphene
import math

from common.methods.send_notification import send_notification
from cs.methods.delivery_methods.get_delivery_price import get_delivery_price
from cs.models import CsRequest
from order.models import OrderMaster, ZipCode, OrderDetail
from order.types.ordered_product import OrderedProductInputType
from product.models import ProductMaster, Product, NewDraft


class AdditionalOrder(graphene.Mutation):
    class Arguments:
        cs_request_id = graphene.Int()
        ordered_products = graphene.List(OrderedProductInputType)

    success = graphene.Boolean()
    message = graphene.String()

    @classmethod
    def mutate(cls, _, __, cs_request_id, ordered_products):
        try:
            cs_request = CsRequest.objects.get(pk=cs_request_id)
            user = cs_request.gym.user
            old_order_master = cs_request.order_master
            # 도서산간 추가배송비
            extra_delivery = ZipCode.objects.filter(zip_code=user.gym.zip_code).first()
            extra_delivery_price = extra_delivery.additional_delivery_price if extra_delivery else 0
            total_delivery_price = get_delivery_price(ordered_products=ordered_products, extra_delivery_price=extra_delivery_price)

            is_pick_up = old_order_master.is_pick_up
            final_delivery_price = 0 if is_pick_up else total_delivery_price

            new_order_master = OrderMaster.objects.create(user=user, receiver=user.gym.name,
                                                          order_number='O{}{}'.format(user.phone[-4:],datetime.now().strftime('%y%m%d%H%M%S')),
                                                          phone=user.phone,
                                                          zip_code=user.gym.zip_code,
                                                          address=user.gym.address,
                                                          detail_address=user.gym.detail_address,
                                                          price_delivery=final_delivery_price,
                                                          is_pick_up=is_pick_up,
                                                          parent_order=cs_request.order_master)
            gym = cs_request.gym
            total_price = 0
            for index, ordered_product in enumerate(ordered_products):
                product = Product.objects.get(pk=ordered_product.product_id)
                product_master = product.product_master
                price_total = product.product_master.price_gym + product.price_additional
                draft = None
                if ordered_product.draft_id:
                    draft = NewDraft.objects.get(pk=ordered_product.draft_id)
                    price_total += draft.price_work
                students_name_list = ordered_product.student_names if ordered_product.student_names else []
                total_price += price_total * ordered_product.quantity
                order_detail = OrderDetail.objects.create(order_master=new_order_master,
                                                          state="간편주문",
                                                          order_detail_number=new_order_master.order_number + str(
                                                              index),
                                                          product_master=product.product_master,
                                                          product=product,
                                                          quantity=ordered_product.quantity,
                                                          user_request=ordered_product.user_request,
                                                          new_draft=draft,
                                                          price_option=product.price_additional * ordered_product.quantity,
                                                          price_total=price_total * ordered_product.quantity,
                                                          price_products=product.product_master.price_gym * ordered_product.quantity,
                                                          price_work=draft.price_work * ordered_product.quantity if draft is not None else 0,
                                                          price_work_labor=draft.price_work_labor * ordered_product.quantity if draft is not None else 0,
                                                          student_names=students_name_list,
                                                          price_consumer=product_master.price_consumer,
                                                          price_parent=product_master.price_parent,
                                                          price_gym=product_master.price_gym,
                                                          price_vendor=product_master.price_vendor
                                                          )
                gym.total_purchased_amount += order_detail.price_gym * order_detail.quantity + order_detail.price_work
                gym.save()
            send_notification(user=new_order_master.user, type="간편주문 결제요청", product_names=new_order_master.order_name,
                              order_master=new_order_master)
            return AdditionalOrder(success=True, message="추가주문이 완료되었습니다.")
        except Exception as e:
            import logging
            logger = logging.getLogger('myLog')
            logger.info(e)
            return AdditionalOrder(success=False, message="오류가 발생하였습니다. 개발팀에 문의해주세요")
