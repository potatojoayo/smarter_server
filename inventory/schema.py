import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField

from inventory.models import Supplier, ChangeHistory
from inventory.mutations.add_inventory_order_details import AddInventoryOrderDetails
from inventory.mutations.change_inventory_quantity import ChangeInventoryQuantity
from inventory.mutations.create_inventory_order import CreateInventoryOrder
from inventory.mutations.create_inventory_received import CreateInventoryReceived
from inventory.mutations.create_new_inventory import CreateNewInventory
from inventory.mutations.delete_inventory_order_details import DeleteInventoryOrderDetails
from inventory.mutations.start_inventory_order import StartInventoryOrder
from inventory.mutations.save_inventory_order import SaveInventoryOrder
from inventory.mutations.update_inventory_order import UpdateInventoryOrder
from inventory.mutations.update_supplier import UpdateSupplier
from inventory.mutations.additional_receive import AdditionalReceive
from inventory.types.change_history_node import ChangeHistoryNode
from inventory.types.change_history_type import ChangeHistoryType
from inventory.types.inventory_order.inventory_order_master_node import InventoryOrderMasterNode
from inventory.types.inventory_received_detail_node import InventoryReceivedDetailNode
from inventory.types.inventory_received_master_node import InventoryReceivedMasterNode
from inventory.types.supplier_type import SupplierType


class Query(graphene.ObjectType):
    suppliers = graphene.List(SupplierType)
    supplier = graphene.Field(SupplierType, id=graphene.ID())
    change_history = graphene.Field(ChangeHistoryType)
    change_histories = DjangoFilterConnectionField(ChangeHistoryNode)

    inventory_received_master = relay.Node.Field(InventoryReceivedMasterNode)
    inventory_received_masters = DjangoFilterConnectionField(InventoryReceivedMasterNode)
    inventory_received_details = DjangoFilterConnectionField(InventoryReceivedDetailNode)

    inventory_orders = DjangoFilterConnectionField(InventoryOrderMasterNode)
    inventory_order = relay.Node.Field(InventoryOrderMasterNode)

    @staticmethod
    def resolve_suppliers(_, __):
        return Supplier.objects.all()

    @staticmethod
    def resolve_supplier(_, __, id):
        return Supplier.objects.get(pk=id)

    @staticmethod
    def resolve_change_history(_, __):
        return ChangeHistory.objects.all()


class Mutation(graphene.ObjectType):
    update_supplier = UpdateSupplier.Field()
    change_inventory_quantity = ChangeInventoryQuantity.Field()
    create_inventory_received = CreateInventoryReceived.Field()
    create_inventory_order = CreateInventoryOrder.Field()
    start_inventory_order = StartInventoryOrder.Field()
    save_inventory_order = SaveInventoryOrder.Field()
    delete_inventory_order_details = DeleteInventoryOrderDetails.Field()
    add_inventory_order_details = AddInventoryOrderDetails.Field()
    update_inventory_order = UpdateInventoryOrder.Field()
    create_new_inventory = CreateNewInventory.Field()
    additional_receive = AdditionalReceive.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)



