from graphene_django import DjangoObjectType

from cs.models import ChangeRequest
import graphene

from cs.types.change_types.change_detail_type import ChangeDetailType


class ChangeRequestType(DjangoObjectType):
    class Meta:
        model = ChangeRequest

    cs_request_number = graphene.String()
    order_number = graphene.String()
    gym_name = graphene.String()
    change_products_name = graphene.String()
    change_details = graphene.List(ChangeDetailType)
    total_change_details = graphene.Int()
    delivery = graphene.Field('order.types.delivery_type.DeliveryType')

    @staticmethod
    def resolve_delivery(root: ChangeRequest, __):
        return root.delivery

    customer = graphene.Field('business.types.GymType')

    @staticmethod
    def resolve_customer(root: ChangeRequest, __):
        if root.cs_request:
            return root.cs_request.gym
        else:
            return root.user.gym
        # return root.cs_request.gym

    @staticmethod
    def resolve_cs_request_number(root, _):
        if root.cs_request:
            return root.cs_request.request_number
        else:
            return None
        # return root.cs_request.request_number
    @staticmethod
    def resolve_order_number(root, _):
        if root.cs_request:
            return root.cs_request.order_master.order_number
        else:
            change_request_detail = root.change_details.all().first()
            return change_request_detail.order_detail.order_master.order_number
        # return root.cs_request.order_master.order_number
    @staticmethod
    def resolve_gym_name(root, _):
        if root.cs_request:
            return root.cs_request.gym.name
        else:
            return root.user.gym.name
        # return root.cs_request.gym.name

    @staticmethod
    def resolve_change_products_name(root, __):
        detail_count = root.change_details.all().count()
        detail = root.change_details.all().first()
        first_product_name = detail.changed_product.product_master.name
        if detail_count == 1:
            return first_product_name
        else:
            return first_product_name + ' 외 {}건'.format(detail_count - 1)
    @staticmethod
    def resolve_change_details(root: ChangeRequest, __):
        return root.change_details.all().order_by('id')


    @staticmethod
    def resolve_total_change_details(root, __):
        return root.change_details.all().count()
