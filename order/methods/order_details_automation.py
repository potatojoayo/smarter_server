from business.models import Subcontractor
from order.models import Work


def order_details_automation(order_details, order_master):
    order_details_pre_work = []
    order_details_belt = []
    ## order master는 같지만 order detail의 subcontractor가 다른 경우, 같은 애들끼리 묶어주기 위한 프로세스
    for order_detail in order_details:
        if order_detail.new_draft:
            if order_detail.product_master.category.name == "벨트":
                order_detail.state = "후작업중"
                order_details_belt.append(order_detail)
            else:
                order_detail.state = "전처리작업중"
                order_details_pre_work.append(order_detail)
        else:
            order_detail.state = "출고준비"
        order_detail.save()

    subcontractor_pre_work = Subcontractor.objects.get(name="전처리작업실")
    subcontractor_belt = Subcontractor.objects.get(name="띠자수작업실")

    if len(order_details_pre_work) > 0 :
        pre_work = Work.objects.create(order_master=order_master,
                                       subcontractor=subcontractor_pre_work)
        for order_detail_pre_work in order_details_pre_work:
            order_detail_pre_work.work= pre_work
            order_detail_pre_work.save()
    if len(order_details_belt) > 0 :
        belt_work = Work.objects.create(order_master=order_master,
                                        subcontractor=subcontractor_belt)
        for order_detail_belt_work in order_details_belt:
            order_detail_belt_work.work = belt_work
            order_detail_belt_work.save()


