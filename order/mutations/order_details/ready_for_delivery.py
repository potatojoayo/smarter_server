# 각 상태(state)를 바꿔주는 mutation
from datetime import datetime

import graphene
from django.db import transaction

from common.methods.send_notification import send_notification
from order.models import OrderDetail, OrderMaster


class ReadyForDelivery(graphene.Mutation):
    class Arguments:
        order_detail_numbers = graphene.List(graphene.String)

    success = graphene.Boolean()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, info, order_detail_numbers):
        order_details = OrderDetail.objects.filter(order_detail_number__in=order_detail_numbers)
        now = datetime.today()
        deadline = datetime(now.year, now.month, now.day, 14, 0, 0)
        for order_detail in order_details:
            if now < deadline and not order_detail.order_master.is_pick_up:
                user = order_detail.order_master.user
                today_order_masters = OrderMaster.objects.filter(
                    user=user,
                    date_created__lte=deadline,
                    details__state__in=['출고준비', '묶음배송']
                ).exclude(pk=order_detail.order_master.id)
                if today_order_masters.count() > 0:
                    for order_master in today_order_masters:
                        order_master.details.filter(state__in=['출고준비', '묶음배송'], product__product_master__delivery_type='일반배송상품').update(state='묶음배송')
                    order_detail.state = '묶음배송'
                    order_detail.save()
                else:
                    order_detail.state = '출고준비'
                    order_detail.save()
            else:
                order_detail.state = '출고준비'
                order_detail.save()
        order_master_list = []
        for order_detail in order_details:
            order_master_dic = {
                'state': "출고준비",
                'order_master': order_detail.order_master,
                'product_name': order_detail.product.name,
                'quantity': 1
            }
            if order_detail.state == "출고준비":
                exist = False
                for order_master in order_master_list:
                    if order_master['order_master'].id == order_master_dic['order_master'].id:
                        order_master['quantity'] += 1
                        exist = True
                if not exist:
                    order_master_list.append(order_master_dic)
            elif order_detail.state == "묶음배송":
                exist = False
                for order_master in order_master_list:
                    if order_master['order_master'].id == order_master_dic['order_master'].id:
                        order_master['quantity'] += 1
                        exist = True
                if not exist:
                    order_master_list.append(order_master_dic)
        print(order_master_list)
        """
        for order_master in order_master_list:
            if order_master['state'] == "출고준비":
                send_notification(user=order_master['order_master'].user, type="출고준비",
                                  product_names=order_master['product_name'], quantity=order_master['quantity'])
            elif order_master['state'] == "묶음배송":
                send_notification(user=order_master['order_master'].user, type="묶음배송",
                                  product_names=order_master['product_name'], quantity=order_master['quantity'])
        """
        return ReadyForDelivery(success=True)


