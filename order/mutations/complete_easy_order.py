import graphene
import math
from datetime import datetime

from common.methods.create_notification import create_notification
from common.methods.send_notification import send_notification
from common.models import Address
from order.models import OrderMaster, EasyOrder, ZipCode, OrderDetail
from order.types.ordered_product import OrderedProductInputType
from product.models import ProductMaster, Product, NewDraft


class CompleteEasyOrder(graphene.Mutation):
    class Arguments:
        easy_order_id = graphene.Int()
        ordered_products = graphene.List(OrderedProductInputType)
        easy_order_is_visit = graphene.Boolean()
        address_id = graphene.Int()
        memo = graphene.String()
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, easy_order_id, ordered_products, easy_order_is_visit, address_id=None, memo=None):
        easy_order = EasyOrder.objects.get(pk=easy_order_id)
        product_masters = {}
        for ordered_product in ordered_products:
            product_master_id = str(ordered_product.product_master_id)
            if product_master_id in product_masters:
                product_masters[product_master_id]['quantity'] += ordered_product.quantity
            else:
                product_masters[product_master_id] = {
                    'quantity': ordered_product.quantity
                }
        delivery_price_normals = [0]
        delivery_price_divisions = [0]
        delivery_price_individuals = [0]

        # 도서산간 추가배송비
        extra_delivery = ZipCode.objects.filter(zip_code=easy_order.user.gym.zip_code).first()
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


        total_delivery_price = 0
        is_pick_up = False
        if easy_order_is_visit or easy_order.is_order_more:
            is_pick_up = True
            address = easy_order.user.gym.address
            detail_address = easy_order.user.gym.detail_address
            zip_code = easy_order.user.gym.zip_code
        else:
            total_delivery_price = max(delivery_price_normals) + sum(delivery_price_divisions) + sum(
                delivery_price_individuals)
            user_address = Address.objects.get(pk=address_id)
            address = user_address.address
            detail_address = user_address.detail_address
            zip_code = user_address.zip_code
        order_master = OrderMaster.objects.create(user=easy_order.user, receiver=easy_order.user.gym.name,
                                                  order_number='O{}{}'.format(easy_order.user.phone[-4:],
                                                                              datetime.now().strftime('%y%m%d%H%M%S')),
                                                  phone=easy_order.user.phone,
                                                  zip_code=zip_code,
                                                  memo_by_admin=memo,
                                                  address=address,
                                                  detail_address=detail_address,
                                                  price_delivery=total_delivery_price,
                                                  is_pick_up = is_pick_up)

        for index, ordered_product in enumerate(ordered_products):
            product = Product.objects.get(pk=ordered_product.product_id)
            product_master = product.product_master
            price_total = product.product_master.price_gym + product.price_additional
            print(ordered_product)
            if ordered_product.draft_id:
                draft = NewDraft.objects.get(pk=ordered_product.draft_id)
                price_total += draft.price_work
                print(price_total)
                # order detail 생성
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
                                                          student_names=ordered_product.student_names,
                                                          price_consumer=product_master.price_consumer,
                                                          price_parent=product_master.price_parent,
                                                          price_gym=product_master.price_gym,
                                                          price_vendor=product_master.price_vendor,
                                                          )
                gym = order_detail.order_master.user.gym
                gym.total_purchased_amount += order_detail.price_gym * order_detail.quantity + order_detail.price_work
                gym.save()
            else:
                order_detail = OrderDetail.objects.create(order_master=order_master,
                                                          state="간편주문",
                                                          order_detail_number=order_master.order_number + str(index),
                                                          product_master=product.product_master,
                                                          product=product,
                                                          quantity=ordered_product.quantity,
                                                          user_request=ordered_product.user_request,
                                                          price_option=product.price_additional * ordered_product.quantity,
                                                          price_total=price_total * ordered_product.quantity,
                                                          price_products=product.product_master.price_gym * ordered_product.quantity,
                                                          student_names=ordered_product.student_names,
                                                          price_consumer=product_master.price_consumer,
                                                          price_parent=product_master.price_parent,
                                                          price_gym=product_master.price_gym,
                                                          price_vendor=product_master.price_vendor
                                                          )
                gym = order_detail.order_master.user.gym
                gym.total_purchased_amount += order_detail.price_products
                gym.save()

            if ordered_product.is_direct_delivery:
                order_detail.is_direct_delivery = ordered_product.is_direct_delivery
            if ordered_product.date_to_be_shipped:
                order_detail.date_to_be_shipped = datetime.strptime(ordered_product.date_to_be_shipped, '%Y-%m-%d').date()

        EasyOrder.objects.filter(pk=easy_order_id).update(order=order_master, state='주문완료',
                                                          date_completed=datetime.now())
        send_notification(user=order_master.user, type="간편주문 결제요청", product_names=order_master.order_name,
                          order_master=order_master)

        return CompleteEasyOrder(success=True)
