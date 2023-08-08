from datetime import datetime
import graphene

from inventory.models import InventoryOrderMaster, Supplier


class CreateNewInventory(graphene.Mutation):
    class Arguments:
        None

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, **kwargs):
        supplier = Supplier.objects.all().first()
        number = 'I{}'.format(datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3])
        InventoryOrderMaster.objects.create(inventory_order_number=number, state="발주대기", supplier=supplier)

        return CreateNewInventory(success=True)