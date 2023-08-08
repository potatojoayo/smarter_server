from datetime import datetime

import graphene
import math

from authentication.models import User
from business.models import Gym
from cs.methods.delivery_methods.get_delivery_price import get_delivery_price
from order.models import OrderMaster, ZipCode, OrderDetail, TaOrderMaster, TaOrderDetail
from order.types.ordered_product import OrderedProductInputType
from product.models import ProductMaster, Product, NewDraft


class CreateTaOrder(graphene.Mutation):
    class Arguments:
        gym_id = graphene.Int()
        ordered_products = graphene.List(OrderedProductInputType)
        address = graphene.String()
        detail_address = graphene.String()
        zip_code = graphene.String()

    success = graphene.Boolean()
    message = graphene.String()

    @classmethod
    def mutate(cls, _, info, gym_id, ordered_products, address, detail_address, zip_code):
        try:
            user = info.context.user
            print(user)
            gym = user.gym
            ta_firm = user.ta_firm
            customer_gym = Gym.objects.get(pk=gym_id)
            customer_user = customer_gym.user
            # 도서산간 추가배송비
            extra_delivery = ZipCode.objects.filter(zip_code=zip_code).first()
            extra_delivery_price = extra_delivery.additional_delivery_price if extra_delivery else 0
            total_delivery_price = get_delivery_price(ordered_products=ordered_products, extra_delivery_price=extra_delivery_price)
            order_master = OrderMaster.objects.create(user=user, receiver=customer_user.name,
                                                      order_number='O{}{}'.format(customer_user.phone[-4:],datetime.now().strftime('%y%m%d%H%M%S')),
                                                      phone=customer_user.phone,
                                                      zip_code=zip_code,
                                                      address=address,
                                                      detail_address=detail_address,
                                                      price_delivery=total_delivery_price,
                                                      is_pick_up=False)
            ta_order_master = TaOrderMaster.objects.create(ta_firm=ta_firm,
                                                           order_master=order_master,
                                                           order_number=order_master.order_number,
                                                           gym_name=customer_gym.name,
                                                           price_paid=0,
                                                           price_delivery=total_delivery_price,
                                                           price_to_be_paid=0
                                                           )
            price_to_be_paid = total_delivery_price
            for index, ordered_product in enumerate(ordered_products):
                product = Product.objects.get(pk=ordered_product.product_id)
                product_master = product.product_master
                price_total = product.product_master.price_gym + product.price_additional
                draft = None
                if ordered_product.draft_id:
                    draft = NewDraft.objects.get(pk=ordered_product.draft_id)
                    price_total += draft.price_work
                order_detail = OrderDetail.objects.create(order_master=order_master,
                                                          state="간편주문",
                                                          order_detail_number=order_master.order_number + str(index),
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
                                                          student_names=ordered_product.student_names if ordered_product.student_names is not None else [],
                                                          price_consumer=product_master.price_consumer,
                                                          price_parent=product_master.price_parent,
                                                          price_gym=product_master.price_gym,
                                                          price_vendor=product_master.price_vendor)
                price_to_be_paid += order_detail.price_gym
                TaOrderDetail.objects.create(ta_order_master=ta_order_master,
                                             order_detail=order_detail,
                                             price_special=order_detail.price_gym,
                                             total_price_special=order_detail.price_gym * order_detail.quantity)

                gym.total_purchased_amount += order_detail.price_gym * order_detail.quantity + order_detail.price_work
                gym.save()
            ta_order_master.price_to_be_paid = price_to_be_paid
            ta_order_master.save()
            return CreateTaOrder(success=True, message="주문이 완료되었습니다.")
        except Exception as e:
            import logging
            print(e)
            logger = logging.getLogger('myLog')
            logger.info('create_ta_order 뮤테이션')
            logger.info(e)
            return CreateTaOrder(success=False, message="오류가 발생하였습니다")

