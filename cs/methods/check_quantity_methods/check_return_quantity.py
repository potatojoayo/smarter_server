from django.db.models import Q

from cs.models import ReturnRequestDetail
from order.models import OrderDetail


def check_return_quantity(return_details):
    for return_detail in return_details:
        old_return_detail = ReturnRequestDetail.objects.get(pk=return_detail.id)
        order_detail_number = old_return_detail.order_detail.order_detail_number
        q = Q()
        q.add(Q(state__in="교환") | Q(state__in="반품"), q.AND)
        old_order_detail = OrderDetail.objects.filter(order_detail_number=order_detail_number).exclude(q).first()
        if old_order_detail.quantity + old_return_detail.return_quantity < return_detail.return_quantity:
            return False, "{} 의 반품갯수를 {}개 이하로 설정해주세요.".format(old_order_detail.product.name, old_order_detail.quantity + old_return_detail.return_quantity)
    return True, 'OK'