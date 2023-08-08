# 작업중 눌렀을때 mutation

import graphene
from django.contrib.auth.models import Group

from authentication.models import User
from business.models import Subcontractor
from common.methods.create_notification import create_notification
from common.methods.send_notification import send_notification
from order.models import Work, WorkDetail
from order.models.order_detail import OrderDetail

from django.db import transaction


class AssignWork(graphene.Mutation):
    class Arguments:
        order_detail_ids = graphene.List(graphene.Int)
        subcontractor_id = graphene.Int(required=True)
        memo = graphene.String()

    success = graphene.Boolean()
    not_applicable = graphene.Boolean()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, order_detail_ids, subcontractor_id, memo=None):
        order_master_dic = {}
        order_details = OrderDetail.objects.filter(pk__in=order_detail_ids)
        subcontractor = Subcontractor.objects.get(pk=subcontractor_id)
        if subcontractor.name == '전처리작업실':
            for detail in order_details:
                if detail.product_master.category.name not in ['도복', '티셔츠']:
                    return AssignWork(not_applicable=True, success=False)

        for order_detail in order_details:
            order_master_id = order_detail.order_master.id
            if order_master_id in order_master_dic.keys():
                order_master_dic[order_master_id].append(order_detail)
            else:
                order_master_dic[order_master_id] = [order_detail]

        for key, order_details in order_master_dic.items():
            order_master_id = key
            work = Work.objects.create(order_master_id=order_master_id,
                                       subcontractor=subcontractor)
            print(work)
            for order_detail in order_details:
                order_detail.work = work
                order_detail.save()
                if work.subcontractor.is_pre_working:
                    order_detail.state = "전처리작업중"
                    order_detail.save()
                elif work.subcontractor.is_out_working:
                    order_detail.state = "외부작업"
                    order_detail.save()
                else:
                    order_detail.state = "후작업중"
                    order_detail.save()


            # 사용자
            gym_user = work.order_master.user
            # 작업자
            """
            if len(order_details) == 1:
                order_name = order_details[0].product.name
            else:
                order_name = '{} 외 {}개의 상품'.format(order_details[0].product.name, len(order_details)-1)
            
            if work.subcontractor.is_pre_working:
                send_notification(user=gym_user, type="작업실배정", subcontractor=subcontractor)
            elif not work.subcontractor.is_pre_working:
                send_notification(user=gym_user, type="후작업중", subcontractor=subcontractor, order_name=order_name)
            """
        return AssignWork(success=True)



