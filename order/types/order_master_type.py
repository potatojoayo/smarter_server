import graphene
from graphene_django import DjangoObjectType

from cs.methods.get_order_state import get_order_state
from cs.types.coupon_types.coupon_type import CouponType
from order.models import OrderMaster
from order.types.order_detail_type import OrderDetailType
from payment.models import PaymentSuccess, PaymentRequest
from payment.types.payment_request_type import PaymentRequestType
from payment.types.payment_success_type import PaymentSuccessType
from smarter_money.types.smarter_money_history_type import SmarterMoneyHistoryType


class OrderMasterType(DjangoObjectType):
    class Meta:
        model = OrderMaster

    details = graphene.List(OrderDetailType)
    order_details = graphene.List(OrderDetailType)
    order_name = graphene.String()
    payment_success = graphene.Field(PaymentSuccessType)
    payment_request = graphene.Field(PaymentRequestType)
    order_master_id = graphene.Int()
    price_to_pay = graphene.Int()
    price_total = graphene.Int()
    smarter_money_history = graphene.Field(SmarterMoneyHistoryType)
    price_total_products = graphene.Int()
    order_state = graphene.String()
    smarter_money = graphene.Int()
    memo = graphene.String()
    gym_name = graphene.String()
    agency_name = graphene.String()
    orderer = graphene.String()
    additional_orders = graphene.List(lambda: OrderMasterType)
    additional_order_details = graphene.List(OrderDetailType)
    coupon = graphene.Field(CouponType)
    is_child = graphene.Boolean()

    @staticmethod
    def resolve_is_child(root: OrderMaster, _):
        return root.parent_order is not None

    @staticmethod
    def resolve_additional_orders(root:OrderMaster, _):
        return root.children.all().order_by('id')

    @staticmethod
    def resolve_additional_order_details(root: OrderMaster, _):
        children_order_masters = root.children.all()
        order_details = []
        for order_master in children_order_masters:
            order_details.extend(order_master.details.filter(is_deleted=False))
        return order_details

    @staticmethod
    def resolve_gym_name(root: OrderMaster, _):
        return root.user.gym.name

    @staticmethod
    def resolve_agency_name(root: OrderMaster, _):
        return root.user.gym.agency.name if root.user.gym.agency else None

    @staticmethod
    def resolve_orderer(root: OrderMaster, _):
        return root.user.name

    @staticmethod
    def resolve_order_state(root: OrderMaster, _):
        return get_order_state(root)

    @staticmethod
    def resolve_memo(root, _):
        return root.memo_by_admin

    @staticmethod
    def resolve_price_total(root, _):
        return root.price_total

    @staticmethod
    def resolve_smarter_money(root, _):
        money = 0
        for smarter_money_history in root.smarter_money_history.filter(transaction_type='사용'):
            money += smarter_money_history.amount
        return money

    @staticmethod
    def resolve_details(root: OrderMaster, _):
        return root.details.filter(is_deleted=False).order_by('id')

    @staticmethod
    def resolve_smarter_money_history(root, _):
        history = root.smarter_money_history.all()
        if history.count() > 0:
            return history.first()
        return None

    @staticmethod
    def resolve_order_name(root, _):
        return root.order_name

    @staticmethod
    def resolve_order_master_id(root, _):
        return root.id

    @staticmethod
    def resolve_order_details(root, _):
        return root.details.filter(is_deleted=False).order_by('product_id')

    @staticmethod
    def resolve_payment_success(root, _):
        payment = PaymentSuccess.objects.filter(orderId=root.order_number)
        if payment.count() == 0:
            return None
        return payment.first()

    @staticmethod
    def resolve_payment_request(root, _):
        payment = PaymentRequest.objects.filter(orderId=root.order_number)
        if payment.count() == 0:
            return None
        return payment.first()

    @staticmethod
    def resolve_price_total_products(root, _):
        return root.price_total_products

    @staticmethod
    def resolve_coupon(root, _):
        return root.coupon