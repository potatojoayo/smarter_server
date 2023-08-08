

def get_order_state_detail(order_details) -> str:
    order_state = '결제전'

    if order_details.filter(state__icontains="배송"):
        order_state = "배송"
    elif order_details.filter(state__icontains="작업"):
        order_state = "작업"
    elif order_details.filter(state__icontains="결제완료"):
        order_state = "결제완료"
    print(order_state)
    return order_state
