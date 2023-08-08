from django.db.models import Q

from cs.models import ChangeRequestDetail
from order.models import OrderDetail


def check_change_quantity(change_details):
    for change_detail in change_details:
        old_change_detail = ChangeRequestDetail.objects.get(pk=change_detail.id)
        order_detail_number = old_change_detail.order_detail.order_detail_number
        q = Q()
        q.add(Q(state__in="교환") | Q(state__in="반품"), q.AND)
        old_order_detail = OrderDetail.objects.filter(order_detail_number=order_detail_number).exclude(q).first()
        if old_order_detail.quantity + old_change_detail.changing_quantity < change_detail.changing_quantity:
            return False, "{} 의 교환갯수를 {}개 이하로 설정해주세요.".format(old_order_detail.product.name, old_order_detail.quantity + old_change_detail.changing_quantity)
    return True, 'OK'