def append_notification_list(order_detail, notification_list, state):
    notification_object = list(filter(lambda n: n['user'].id == order_detail.order_master.user.id, notification_list))
    if len(notification_object) == 0:
        notification_list.append(
            {'user': order_detail.order_master.user, 'type': state, 'product_names': [order_detail.product.name]})
    else:
        notification = notification_object[0]
        notification['product_names'].append(order_detail.product.name)