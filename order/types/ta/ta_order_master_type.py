import graphene
from graphene_django import DjangoObjectType

from order.models import TaOrderMaster
from order.types.ta.ta_order_detail_type import TaOrderDetailType


class TaOrderMasterType(DjangoObjectType):
    class Meta:
        model = TaOrderMaster

    ta_order_details = graphene.List(TaOrderDetailType)
    total_count = graphene.Int()
    total_price_special = graphene.Int()
    total_price_gym = graphene.Int()

    @staticmethod
    def resolve_total_price_gym(root: TaOrderMaster, _):
        return root.order_master.price_total_products

    @staticmethod
    def resolve_ta_order_details(root, __):
        return root.ta_order_details.filter(is_deleted=False)

    @staticmethod
    def resolve_total_count(root, __):
        return root.ta_order_details.filter(is_deleted=False).count()

    @staticmethod
    def resolve_total_price_special(root, __):

        return root.total_price_special

    ## 주문정보

    ta_name = graphene.String()
    orderer_name = graphene.String()
    phone = graphene.String()
    address = graphene.String()
    detail_address = graphene.String()
    zip_code = graphene.String()
    receiver = graphene.String()
    is_pick_up = graphene.Boolean()
    @staticmethod
    def resolve_ta_name(root, __):
        return root.ta_firm.user.gym.name

    @staticmethod
    def resolve_orderer_name(root, __):
        return root.order_master.user.name

    @staticmethod
    def resolve_phone(root, __):
        return root.order_master.user.phone

    @staticmethod
    def resolve_address(root, __):
        return root.order_master.address

    @staticmethod
    def resolve_detail_address(root, __):
        return root.order_master.detail_address

    @staticmethod
    def resolve_zip_code(root, __):
        return root.order_master.zip_code

    @staticmethod
    def resolve_receiver(root: TaOrderMaster, __):
        return root.order_master.receiver

    @staticmethod
    def resolve_is_pick_up(root, __):
        return root.order_master.is_pick_up



