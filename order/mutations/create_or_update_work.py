import graphene

from business.models import Subcontractor
from order.models import Work
from order.models.order_detail import OrderDetail
from order.types.work_type import WorkType
from order.types.work_input_type import WorkInputType


class CreateOrUpdateWork(graphene.Mutation):
    class Arguments:
        work = WorkInputType()
        order_detail_id = graphene.Int()
        subcontractor_id = graphene.Int()

    work = graphene.Field(WorkType)
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, work, order_detail_id, subcontractor_id):

        order_detail = OrderDetail.objects.get(pk=order_detail_id)
        subcontractor = Subcontractor.objects.get(pk=subcontractor_id)
        if work.id:
            new_work = Work.objects.filter(pk=work.id).update(**work)
        else:
            new_work = Work.objects.create(**work, order_detail=order_detail,
                                           subcontractor=subcontractor)

        return CreateOrUpdateWork(work=new_work)
