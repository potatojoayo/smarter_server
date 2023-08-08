import graphene

from order.models import OrderMaster


class UpdateMemo(graphene.Mutation):
    class Arguments:
        order_master_id = graphene.Int()
        memo = graphene.String()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, order_master_id, memo):
        order_master = OrderMaster.objects.get(pk=order_master_id)
        order_master.memo_by_admin = memo
        order_master.save()
        return UpdateMemo(success=True)
