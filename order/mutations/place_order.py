from datetime import datetime

import graphene
import math

from django.contrib.auth.models import Group
from django.db import transaction

from authentication.models import User
from common.methods.create_notification import create_notification
from cs.models import Coupon
from order.models import OrderMaster, ZipCode
from order.models.order_detail import OrderDetail
from order.types.order_master_type import OrderMasterType
from order.types.ordered_product import OrderedProductInputType
from product.models import ProductMaster, Product, Draft, NewDraft


class PlaceOrder(graphene.Mutation):
    class Arguments:
        # ordering_user = OrderingUserInputType()
        user_id = graphene.Int()
        ordered_products = graphene.List(OrderedProductInputType)
        is_pick_up = graphene.Boolean(default_value=False)

    success = graphene.Boolean()
    order_master = graphene.Field(OrderMasterType)

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, info, ordered_products, user_id=None, is_pick_up=False):

        delivery_price_normals = [0]
        delivery_price_divisions = [0]
        delivery_price_individuals = [0]
        if user_id is not None:
            user = User.objects.get(pk=user_id)
        else:
            user = info.context.user

        address = user.addresses.get(default=True)

        if not is_pick_up:
            # product_master가 같은 상품들끼리 묶기
            product_masters = {}
            for ordered_product in ordered_products:
                product_master_id = str(ordered_product.product_master_id)
                if product_master_id in product_masters:
                    product_masters[product_master_id]['quantity'] += ordered_product.quantity
                else:
                    product_masters[product_master_id] = {
                        'quantity': ordered_product.quantity
                    }

            # 도서산간 추가배송비
            extra_delivery = ZipCode.objects.filter(zip_code=address.zip_code).first()

            # 합친 딕셔너리로 배달비 구하기
            for key, value in product_masters.items():
                product_master = ProductMaster.objects.get(pk=int(key))
                delivery_type = product_master.delivery_type
                quantity = value['quantity']
                price_delivery = product_master.price_delivery
                max_quantity_per_box = product_master.max_quantity_per_box
                # 도서산간 지역의 zip code를 가지고 있으면 추가 배송비 지챈
                if extra_delivery:
                    extra_delivery_price = extra_delivery.additional_delivery_price
                    if delivery_type == '일반배송상품':
                        total_price_delivery = price_delivery + extra_delivery_price
                        delivery_price_normals.append(total_price_delivery)
                    elif delivery_type == '분할배송상품':
                        delivery_price_division = math.ceil(quantity / max_quantity_per_box)
                        total_price_delivery = (price_delivery + extra_delivery_price) * delivery_price_division
                        delivery_price_divisions.append(total_price_delivery)
                    else:
                        total_price_delivery = (price_delivery + extra_delivery_price) * quantity
                        delivery_price_individuals.append(total_price_delivery)
                else:
                    if delivery_type == '일반배송상품':
                        delivery_price_normals.append(price_delivery)
                    elif delivery_type == '분할배송상품':
                        delivery_price_division = math.ceil(quantity / max_quantity_per_box)
                        total_price_delivery = delivery_price_division * price_delivery
                        delivery_price_divisions.append(total_price_delivery)
                    else:
                        total_price_delivery = price_delivery * quantity
                        delivery_price_individuals.append(total_price_delivery)

        total_delivery_price = max(delivery_price_normals) + sum(delivery_price_divisions) + sum(delivery_price_individuals)

        # 주어진 파라미터 + 배달비 넣어주기(order master,order detail 생성)

        # order master 생성
        order_master = OrderMaster.objects.create(user=user, receiver=user.gym.name,
                                                  order_number='O{}{}'.format(user.phone[-4:], datetime.now().strftime('%y%m%d%H%M%S')),
                                                  phone=user.phone,
                                                  zip_code=address.zip_code,
                                                  address=address.address,
                                                  is_pick_up=is_pick_up,
                                                  detail_address=address.detail_address,
                                                  price_delivery=total_delivery_price,
                                                  )

        for index, ordered_product in enumerate(ordered_products):
            product = Product.objects.get(pk=ordered_product.product_id)
            print(product)

            draft = None
            price_total = product.product_master.price_gym + product.price_additional
            if ordered_product.draft_id:
                draft = NewDraft.objects.get(pk=ordered_product.draft_id)
                price_total += draft.price_work
                admin = Group.objects.get(name="관리자")
                admin_users = User.objects.filter(groups=admin)
                # for admin_user in admin_users:
                #     Notification.objects.create(user=admin_user, title="주문요청알림 - 작업실배정필요",
                #                                 contents="{}님께서 주문 요청 및 작업실 배정 요청을 하였습니다.. 작업실 배정해주세요"
                #                                 .format(order_master.order_name),
                #                                 notification_type="주문 및 작업실 배정 요청알림")
            else:
                admin = Group.objects.get(name="관리자")
                admin_users = User.objects.filter(groups=admin)
                # for admin_user in admin_users:
                #     Notification.objects.create(user=admin_user, title="주문요청알림",
                #                                 contents="{}님께서 주문 요청을 하였습니다. 주문관리에서 확인 부탁드립니다."
                #                                 .format(order_master.order_name),
                #                                 notification_type="부분입고완료")

            # order detail 생성
            product_master = product.product_master
            order_detail =OrderDetail.objects.create(order_master=order_master,
                                                     state="구매요청",
                                                     order_detail_number=order_master.order_number+str(index),
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
                                                     student_names=ordered_product.student_names,
                                                     price_consumer=product_master.price_consumer,
                                                     price_parent=product_master.price_parent,
                                                     price_gym=product_master.price_gym,
                                                     price_vendor=product_master.price_vendor
                                                     )

            gym = order_detail.order_master.user.gym
            gym.total_purchased_amount += order_detail.price_gym * order_detail.quantity + order_detail.price_work
            gym.save()
        return PlaceOrder(success=True, order_master=order_master)

