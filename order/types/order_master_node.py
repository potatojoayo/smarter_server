import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from authentication.types import UserType
from base_classes import CountableConnectionBase
from cs.methods.get_order_state import get_order_state
from cs.types.coupon_types.coupon_type import CouponType
from order.models import OrderMaster
from order.types.order_detail_type import OrderDetailType
from payment.models import PaymentSuccess, PaymentRequest
from payment.types.payment_request_type import PaymentRequestType
from payment.types.payment_success_type import PaymentSuccessType
from smarter_money.types.smarter_money_history_type import SmarterMoneyHistoryType


class OrderMasterNode(DjangoObjectType):
    class Meta:
        model = OrderMaster
        filter_fields = {
            "id": ['exact'],
            'date_created': ['lte', 'gte'],
            'user__gym__name': ['icontains'],
        }
        interfaces = (relay.Node,)
        connection_class = CountableConnectionBase

    details = graphene.List(OrderDetailType)
    payment_success = graphene.Field(PaymentSuccessType)
    payment_request = graphene.Field(PaymentRequestType)
    order_master_id = graphene.Int()
    price_to_pay = graphene.Int()
    price_total = graphene.Int()
    price_total_work_labor = graphene.Int()
    price_total_work = graphene.Int()
    price_total_products = graphene.Int()
    smarter_money_history = graphene.Field(SmarterMoneyHistoryType)
    states = graphene.List(graphene.String)
    user = graphene.Field(UserType)
    gym_name = graphene.String()
    agency_name = graphene.String()
    orderer = graphene.String()
    smarter_money = graphene.Int()
    memo = graphene.String()
    order_state = graphene.String()
    has_user_request = graphene.Boolean()

    @staticmethod
    def resolve_has_user_request(root: OrderMaster, _):
        for detail in root.details.all():
            if detail.user_request and len(detail.user_request)>0 :
                return True
        return False

    @staticmethod
    def resolve_order_state(root: OrderMaster, _):
        return get_order_state(root)

    @staticmethod
    def resolve_gym_name(root: OrderMaster, _):
        return root.user.gym.name

    @staticmethod
    def resolve_smarter_money_history(root, _):
        history = root.smarter_money_history.filter(transaction_type='사용')
        if history.count() > 0:
            return history.first()
        return None

    @staticmethod
    def resolve_price_to_pay(root, _):
        return root.price_to_pay

    @staticmethod
    def resolve_order_master_id(root, _):
        return root.id

    @staticmethod
    def resolve_details(root, _):
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
    def resolve_price_total(root, _):
        return root.price_total

    @staticmethod
    def resolve_price_total_work_labor(root, _):
        return root.price_total_work_labor

    @staticmethod
    def resolve_price_total_work(root, _):
        return root.price_total_work

    @staticmethod
    def resolve_price_total_products(root, _):
        return root.price_total_products

    @staticmethod
    def resolve_states(root: OrderMaster, _):
        states = [detail.state for detail in root.details.all()]
        for child in root.children.all():
            states.extend([detail.state for detail in child.details.all()])
        return list(set(states))

    @staticmethod
    def resolve_agency_name(root: OrderMaster, _):
        return root.user.gym.agency.name if root.user.gym.agency else None

    @staticmethod
    def resolve_orderer(root: OrderMaster, _):
        return root.user.name

    @staticmethod
    def resolve_memo(root, _):
        return root.memo_by_admin

    @staticmethod
    def resolve_smarter_money(root, _):
        money = 0
        for smarter_money_history in root.smarter_money_history.filter(transaction_type='사용'):
            money += smarter_money_history.amount
        return money
