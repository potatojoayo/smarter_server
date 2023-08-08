from business.models import Subcontractor
from common.methods.send_notification import send_notification


def belt_assign_work(order_details):
    subcontractor = Subcontractor.objects.get(name="띠자수작업실")
    order_master_list = []
    for order_detail in order_details:
        order_master_dic = {
            'order_master': order_detail.order_master
        }
        exist = False
        for order_master in order_master_list:
            if order_master_dic['order_master'].id == order_master['order_master'].id:
                exist = True
        if not exist:
            order_master_list.append(order_master_dic)
    """for order_master in order_master_list:
        send_notification(user=order_master['order_master'].user, type="작업실배정", subcontractor=subcontractor)
    """


