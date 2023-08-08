from datetime import datetime

import graphene
from graphene_file_upload.scalars import Upload

from common.methods.create_notification import create_notification
from common.methods.send_notification import send_notification
from order.models import OrderDetail, Delivery

from smarter_money.models import SmarterMoneyHistory


class BundleDelivery(graphene.Mutation):
    class Arguments:
        order_detail_ids = graphene.List(graphene.Int)
        delivery_agency_id = graphene.Int()
        tracking_number = graphene.String()
        photo = Upload()
    success = graphene.Boolean()
    @classmethod
    def mutate(cls, _, __, order_detail_ids,
               delivery_agency_id, tracking_number, photo=None):
        delivery = Delivery.objects.create(delivery_agency_id=delivery_agency_id,
                                           tracking_number=tracking_number,
                                           photo=photo)
        order_details = OrderDetail.objects.filter(pk__in=order_detail_ids)
        user = OrderDetail.objects.filter(pk__in=order_detail_ids).first().order_master.user

        products = []
        max_delivery_price = 0
        order_masters = []
        max_order = None
        wallet_delivery_price = 0
        for order_detail in order_details:
            user = order_detail.order_master.user
            products.append(order_detail.product.name)
            order_detail.state = '배송중'
            order_detail.delivery = delivery

            if order_detail.product_master.price_delivery > max_delivery_price:
                max_delivery_price = order_detail.product_master.price_delivery
                max_order = order_detail.order_master
                exists = True
                for order_master in order_masters:
                    if order_detail.order_master.id != order_master.id:
                        exists = False
                if not exists:
                    order_masters.append(order_detail.order_master)
            order_detail.save()

        for order_master in order_masters:
            if order_master.id != max_order.id:
                wallet_delivery_price += order_master.price_delivery

        user.wallet.balance += wallet_delivery_price
        user.wallet.save()
        send_notification(user=user, type="묶음배송중", product_names=products, amount=wallet_delivery_price)

        SmarterMoneyHistory.objects.create(
            history_number='H{}{}'.format(user.phone, datetime.now().strftime('%y%m%d%H%M%S')),
            wallet=user.wallet,
            transaction_type='적립',
            amount=wallet_delivery_price,
            description='묶음배송'
        )
        return BundleDelivery(success=True)

