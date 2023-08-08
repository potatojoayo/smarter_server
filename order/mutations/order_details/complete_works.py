import graphene
from django.contrib.auth.models import Group

from authentication.models import User
from common.methods.create_notification import create_notification
from common.methods.send_notification import send_notification
from order.models import Work


class CompleteWorks(graphene.Mutation):
    class Arguments:
        work_ids = graphene.List(graphene.Int)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, work_ids):
        works = Work.objects.filter(pk__in=work_ids)
        for work in works:
            order_details = work.details.all()
            work.state = "작업완료"
            work.save()
            for order_detail in order_details:
                order_detail.state = "후작업완료"
                order_detail.save()
            # 사용자
            gym_user = work.order_master.user
            # 관리자
            if len(order_details) == 1:
                order_name = order_details[0].product.name
            else:
                order_name = '{} 외 {}개의 상품'.format(order_details[0].product.name, len(order_details)-1)
            #send_notification(user=gym_user, type="후작업완료", product_names=order_name)

        return CompleteWorks(success=True)
