import graphene
from django.db import transaction

from order.models import EasyOrder, OrderMaster


class DeleteOrderMasters(graphene.Mutation):
    class Arguments:
        order_numbers = graphene.List(graphene.String)

    success = graphene.Boolean()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, order_numbers):
        for order_number in order_numbers:
            order_master = OrderMaster.objects.get(order_number=order_number)
            order_master.is_deleted = True
            order_master.save()

            for child in order_master.children.all():
                child.is_deleted = True
                child.save()

        return DeleteOrderMasters(success=True)
