from order.models import OrderMaster


def get_order_state(order_master: OrderMaster) -> str:
    order_state = '결제완료'
    if order_master.details.filter(state__in=['간편주문', '무통장입금']):
        order_state = '결제전'
    if order_master.details.filter(state__icontains="주문취소"):
        order_state = '주문취소'
    elif order_master.details.filter(state__icontains="취소완료"):
        order_state = '주문취소'
    elif order_master.details.filter(state__icontains="배송"):
        order_state = "배송"
    elif order_master.details.filter(state__icontains="작업"):
        order_state = "작업"
    return order_state
