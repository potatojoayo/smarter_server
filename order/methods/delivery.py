from datetime import datetime

from django.contrib.auth.models import Group

from authentication.models import User
from common.methods.append_notification_list import append_notification_list
from common.methods.create_notification import create_notification
from common.methods.send_notification import send_notification

from order.models import OrderDetail


def delivery(order_details):
    now = datetime.today()
    deadline = datetime(now.year, now.month, now.day, 14, 0, 0)
    notification_list = []

    if now < deadline:
        for order_detail in order_details:
            user = order_detail.order_master.user
            today_order_details = OrderDetail.objects.filter(
                order_master__user=user,
                # order_master__date_created__lte=deadline,
                order_master__date_created__lte=now,

                state='출고준비',
                product__product_master__delivery_type='일반배송상품'
            )
            print(today_order_details)
            if today_order_details.count() > 0:
                order_detail.state = '묶음배송'
                state = '묶음배송'
                order_detail.save()
            else:
                order_detail.state = '출고준비'
                order_detail.save()
                state = '출고준비'
            append_notification_list(order_detail=order_detail, notification_list=notification_list,
                                     state=state)
            """
            for notification in notification_list:
                send_notification(user=notification['user'], type=notification['type'],
                                  product_names=notification['product_names'])
            """
