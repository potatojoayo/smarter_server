def check_quantity_order_detail(order_detail, state):

    if order_detail.new_draft:
        if order_detail.state == '결제전' or order_detail.state == '결제완료':
            order_detail.product.inventory_quantity += order_detail.quantity
            order_detail.state = '취소완료'
            order_detail.is_deleted = True
            order_detail.product.save()
    else:
        order_detail.product.inventory_quantity += order_detail.quantity
        order_detail.product.save()
    order_detail.save()
    order_detail.product.save()