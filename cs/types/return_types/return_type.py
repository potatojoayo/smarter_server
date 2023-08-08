from graphene_django import DjangoObjectType
import graphene
from cs.models import ReturnRequest
from cs.types.return_types.return_detail_type import ReturnDetailType


class ReturnType(DjangoObjectType):
    class Meta:
        model = ReturnRequest

    cs_request_number = graphene.String()
    order_number = graphene.String()
    return_products_name = graphene.String()
    gym_name = graphene.String()

    return_details = graphene.List(ReturnDetailType)
    total_detail_count = graphene.Int()
    user_id = graphene.Int()

    @staticmethod
    def resolve_user_id(root: ReturnRequest, _):
        if root.cs_request:
            return root.cs_request.gym.user.id
        else:
            return root.user.id
        # return root.cs_request.gym.user.id

    current_user_smarter_money = graphene.Int()

    @staticmethod
    def resolve_current_user_smarter_money(root: ReturnRequest, _):
        if root.cs_request:
            return root.cs_request.gym.user.wallet.balance
        else:
            return root.user.wallet.balance
        # return root.cs_request.gym.user.wallet.balance

    @staticmethod
    def resolve_cs_request_number(root, __):
        if root.cs_request:
            return root.cs_request.request_number
        else:
            return None
        # return root.cs_request.request_number

    @staticmethod
    def resolve_order_number(root, __):
        if root.cs_request:
            return root.cs_request.order_master.order_number
        else:
            return_detail = root.return_details.all().first()
            return return_detail.order_detail.order_master.order_number
        # return root.cs_request.order_master.order_number

    @staticmethod
    def resolve_return_products_name(root, __):
        detail_count = root.return_details.all().count()
        detail = root.return_details.all().first()
        first_product_name = detail.order_detail.product_master.name
        if detail_count == 1:
            return first_product_name
        else:
            return first_product_name + " 외 {}건".format(detail_count - 1)

    @staticmethod
    def resolve_gym_name(root, __):
        if root.cs_request:
            return root.cs_request.gym.name
        else:
            return root.user.gym.name
        # return root.cs_request.gym.name

    @staticmethod
    def resolve_return_details(root: ReturnRequest, __):
        return root.return_details.all()

    @staticmethod
    def resolve_total_detail_count(root, __):
        return root.return_details.all().count()
