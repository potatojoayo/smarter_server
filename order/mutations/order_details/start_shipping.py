import graphene
from django.contrib.auth.models import Group
from graphene_file_upload.scalars import Upload

from authentication.models import User
from common.methods.append_notification_list import append_notification_list
from common.methods.create_notification import create_notification
from common.methods.send_notification import send_notification
from common.models import Notification
from order.models import Delivery, OrderDetail


class StartShipping(graphene.Mutation):
    class Arguments:
        order_detail_ids = graphene.List(graphene.Int)
        delivery_agency_id = graphene.Int()
        tracking_number = graphene.String()
        photo = Upload(required=False)

    success = graphene.Boolean(default_value=False)

    @classmethod
    def mutate(cls, _, __, order_detail_ids, delivery_agency_id, tracking_number, photo=None):
        delivery = Delivery.objects.create(delivery_agency_id=delivery_agency_id,
                                           tracking_number=tracking_number,
                                           photo=photo)

        for order_detail_id in order_detail_ids:
            OrderDetail.objects.filter(pk=order_detail_id).update(delivery=delivery, state='배송중')
            order_detail = OrderDetail.objects.get(pk=order_detail_id)
            user = order_detail.order_master.user
            gym_name = user.gym.name
            product = order_detail.product
        order_details = OrderDetail.objects.filter(pk__in=order_detail_ids)
        notification_list = []
        for order_detail in order_details:
            append_notification_list(order_detail=order_detail,
                                     notification_list=notification_list,
                                     state="배송중")

        for notification in notification_list:
            send_notification(user=notification['user'],
                              type=notification['type'],
                              product_names=notification['product_names'])

        return StartShipping(success=True)
