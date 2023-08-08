from django.contrib.auth.models import Group

from authentication.models import User
from common.methods.create_notification import create_notification


def cs_request_send_notification(user=None, type=None, order_master=None, ):
    admin = Group.objects.get(name="관리자")
    admin_users = User.objects.filter(groups=admin)
    if type=="유저주문취소":
        contents = '{}님께서 {} 주문건에 대해 주문취소 요청을 하였습니다.'.format(user.name, order_master.order_number)
        for admin_user in admin_users:
            create_notification.delay(user_id=admin_user.id,
                                      title="유저주문취소",
                                      notification_type="주문취소",
                                      contents=contents)


