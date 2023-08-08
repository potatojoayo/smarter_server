import graphene
from django.db import transaction

from product.models import ProductMaster
from product.types.product_master.change_display_order_input_type import ChangeDisplayOrderInputType


class ChangeDisplayOrder(graphene.Mutation):

    class Arguments:
        changing_product_masters = graphene.List(ChangeDisplayOrderInputType)

    success = graphene.Boolean(default_value=False)

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, changing_product_masters):
        try:
            for changing_product_master in changing_product_masters:
                ProductMaster.objects.filter(pk=changing_product_master.product_master_id).update(display_order=changing_product_master.display_order)
            return ChangeDisplayOrder(success=True)
        except Exception:
            return ChangeDisplayOrder(success=False)



