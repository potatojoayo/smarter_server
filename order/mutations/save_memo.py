import graphene

from order.models import OrderMaster


class SaveMemo(graphene.Mutation):
    class Arguments:
        order_master_id = graphene.Int()
        memo = graphene.String()

    success = graphene.Boolean(default_value=False)

    @classmethod
    def mutate(cls, _, __, order_master_id, memo):
        try:
            order_master = OrderMaster.objects.get(pk=order_master_id)
            order_master.memo_by_admin = memo
            order_master.save()
            return SaveMemo(success=True)
        except Exception as e:
            print(e)
            return SaveMemo()
