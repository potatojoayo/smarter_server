import graphene

from order.models import OrderMaster


class ToggleActive(graphene.Mutation):
    class Arguments:
        order_master_id = graphene.Int()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, order_master_id):
        order_master = OrderMaster.objects.get(pk=order_master_id)
        order_master.is_active = not order_master.is_active
        order_master.save()
        return ToggleActive(success=True)