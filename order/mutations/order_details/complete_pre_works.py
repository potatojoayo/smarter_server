import graphene

from business.models import Subcontractor
from common.methods.create_notification import create_notification
from common.methods.send_notification import send_notification
from order.models import Work


class CompletePreWorks(graphene.Mutation):
    class Arguments:
        work_ids = graphene.List(graphene.Int)
        subcontractor_id = graphene.Int()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, work_ids, subcontractor_id):
        subcontractor = Subcontractor.objects.get(pk=subcontractor_id)
        for work_id in work_ids:
            work = Work.objects.get(pk=work_id)
            work.subcontractor = subcontractor
            work.save()
            order_details = work.details.all()
            for order_detail in order_details:
                order_detail.state = "후작업중"
                order_detail.save()
            gym_user = work.order_master.user
            print(order_details)
            if len(order_details) == 1:
                order_name = order_details[0].product.name
            else:
                order_name = '{} 외 {}개의 상품'.format(order_details[0].product.name, len(order_details) - 1)
            #send_notification(user=gym_user, type="후작업중",order_name=order_name,
            #                  subcontractor=subcontractor)
        return CompletePreWorks(success=True)