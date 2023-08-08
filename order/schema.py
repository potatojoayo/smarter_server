from datetime import datetime, timedelta

import graphene
from django.db.models import Q

from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required

from authentication.mutations.me import Me
from cs.models import Coupon
from .fields.distinct_field import DistinctField
from .fields.my_easy_order_field import MyEasyOrderField
from .fields.my_order_field import MyOrderField
from .fields.order_master_connection_field import OrderMasterConnectionField
from .fields.work_field import WorkField
from .models import Payment, OrderMaster, EasyOrder, Delivery, Claim, TaOrderMaster, Work
from .models.order_detail import OrderDetail
from .mutations.complete_easy_order import CompleteEasyOrder
from .mutations.create_easy_order import CreateEasyOrder
from .mutations.create_or_update_work import CreateOrUpdateWork
from .mutations.delete_easy_order_requests import DeleteEasyOrderRequests
from .mutations.delete_order_masters import DeleteOrderMasters
from .mutations.deposit_without_account import DepositWithoutAccount
from .mutations.easy_order_to_paid import EasyOrderToPaid
from .mutations.gym_order_history_by_agency import GymOrderHistoryByAgency
from .mutations.order_by_smarter_money import OrderBySmarterMoney
from .mutations.order_details.assign_work import AssignWork
from .mutations.order_details.bundle_delivery import BundleDelivery
from .mutations.order_details.cancel_easy_order import CancelEasyOrder
from .mutations.order_details.cancel_order import CancelOrder
from .mutations.order_details.change_order import ChangeOrder
from .mutations.order_details.change_state import ChangeState
from .mutations.order_details.complete_claim import CompleteClaim
from .mutations.order_details.complete_payments_without_bank import CompletePaymentsWithoutBank
from .mutations.order_details.complete_pre_works import CompletePreWorks
from .mutations.order_details.complete_works import CompleteWorks
from .mutations.order_details.decline_cliam import DeclineClaim
from .mutations.order_details.pick_up import PickUp
from order.mutations.proceed_paid_order_details import ProceedPaidOrderDetails
from order.mutations.proceed_paid_orders import ProceedPaidOrders
from .mutations.order_details.ready_for_delivery import ReadyForDelivery
from .mutations.order_details.refund_order import RefundOrder
from .mutations.order_details.request_claim import RequestClaim
from .mutations.order_details.start_shipping import StartShipping
from .mutations.place_order import PlaceOrder
from .mutations.save_memo import SaveMemo
from .mutations.ta.create_ta_order import CreateTaOrder
from .mutations.ta.update_ta_order import UpdateTaOrder
from .mutations.toggle_active import ToggleActive
from .mutations.update_memo import UpdateMemo
from .mutations.update_work import UpdateWork
from .mutations.order_details.complete_payment import CompletePayment
from .mutations.update_work_memos import UpdateWorkMemos
from .mutations.user_request_mutations.cancel_mutations.user_cancel_order import UserCancelOrder
from .mutations.user_request_mutations.change_mutations.create_user_change_request import CreateUserChangeRequest
from .mutations.user_request_mutations.return_mutations.create_user_return_request import CreateUserReturnRequest

from .types.claim_node import ClaimNode
from .types.claim_type import ClaimType
from .types.delivery_type import DeliveryType
from .types.easy_order_node import EasyOrderNode
from .types.order_detail_type import OrderDetailType
from .types.order_detail_node import OrderDetailNode
from .types.order_detail_with_children_type import OrderDetailsWithChildrenType
from .types.order_master_node import OrderMasterNode
from .types.payment.payment_type import PaymentType
from .types.order_master_type import OrderMasterType
from order.types.work_type import WorkType
from .types.ta.ta_order_master_type import TaOrderMasterType
from .types.ta.ta_order_masters_type import TaOrderMastersType
from .types.work_node import WorkNode
from .fields import EasyOrderField


class Query(graphene.ObjectType):
    today_delivery_order_count_by_state = graphene.Int(state=graphene.String())
    today_cancel_order_count_by_state = graphene.Int(state=graphene.String())
    today_order_count_by_state = graphene.Int(state=graphene.String())
    today_easy_order_count_by_state = graphene.Int(state=graphene.String())
    today_claim_count_by_state = graphene.Int(state=graphene.String())
    my_order = relay.Node.Field(OrderMasterNode)
    my_order_by_order_number = graphene.Field(OrderMasterType, order_number=graphene.String())

    @staticmethod
    def resolve_my_order_by_order_number(_, __, order_number):
        print('오더넘버')
        print(order_number)
        return OrderMaster.objects.get(order_number=order_number)

    my_orders = MyOrderField(OrderMasterNode)
    order_master_node = relay.Node.Field(OrderMasterNode)
    order_master = graphene.Field(OrderMasterType, order_master_id=graphene.Int(), order_number=graphene.String())
    order_masters = OrderMasterConnectionField(OrderMasterNode, keyword=graphene.String(), state=graphene.String())
    payments = graphene.List(PaymentType)
    order_details = graphene.List(OrderDetailType, order_master_id=graphene.Int())
    order_details_with_children = graphene.Field(OrderDetailsWithChildrenType, order_master_id=graphene.Int())

    order_masters_by_ids = graphene.List(OrderMasterType, ids=graphene.List(graphene.Int))

    @staticmethod
    def resolve_order_masters_by_ids(_, __, ids):
        return OrderMaster.objects.filter(pk__in=ids)

    @staticmethod
    def resolve_order_details_with_children(_, __, order_master_id):
        order_master = OrderMaster.objects.get(pk=order_master_id)
        return OrderDetailsWithChildrenType(order_details=order_master.details.all(), added_order_masters=order_master.children.filter(is_deleted=False))

    order_detail_nodes = DistinctField(OrderDetailNode)
    easy_order = relay.Node.Field(EasyOrderNode)
    my_easy_orders = MyEasyOrderField(EasyOrderNode)
    easy_orders = EasyOrderField(EasyOrderNode, keyword=graphene.String())
    delivery = graphene.Field(DeliveryType, delivery_id=graphene.Int(), order_detail_id=graphene.Int())
    claim = graphene.Field(ClaimType)
    works = WorkField(WorkNode, keyword=graphene.String(), ids=graphene.List(graphene.Int))
    work = relay.Node.Field(WorkNode)
    claims = DjangoFilterConnectionField(ClaimNode)
    date_range = graphene.List(graphene.Date)
    order_detail_delivery = graphene.Field(DeliveryType, order_detail_id=graphene.Int())
    work_by_id = graphene.Field(WorkType, work_id=graphene.Int())

    @staticmethod
    def resolve_work_by_id(_, __, work_id):
        return Work.objects.get(pk=work_id)
    @staticmethod
    def resolve_order_detail_delivery(_, __, order_detail_id):
        order_detail = OrderDetail.objects.get(pk=order_detail_id)
        return order_detail.delivery

    @staticmethod
    def resolve_today_claim_count_by_state(_, __, state):
        if state == '전체':
            return Claim.objects.filter(
            ).distinct().count()
        return Claim.objects.filter(
            state=state,
        ).distinct().count()

    @staticmethod
    def resolve_today_order_count_by_state(_, info, state):
        user = info.context.user
        try:
            order_masters = OrderMaster.objects.filter(user__gym__agency=user.agency)
        except:
            order_masters = OrderMaster.objects.all()
        if state == '전체':
            return order_masters.count()
        return order_masters.filter(
            details__state__exact=state,
        ).all().distinct().count()

    @staticmethod
    def resolve_today_easy_order_count_by_state(_, __, state):
        if state == '전체':
            return EasyOrder.objects.filter(
            ).distinct().count()
        return EasyOrder.objects.filter(
            state=state,
        ).distinct().count()

    @staticmethod
    def resolve_today_cancel_order_count_by_state(_, __, state):
        if state == '전체':
            return OrderMaster.objects.filter(
                details__state__in=['취소요청','취소완료'],
            ).distinct().count()
        return OrderMaster.objects.filter(
            details__state=state,
        ).distinct().count()

    @staticmethod
    def resolve_today_delivery_order_count_by_state(_, __, state):
        if state == '전체':
            return OrderMaster.objects.filter(
                details__state__in=['출고준비','추후배송', '배송중', '배송완료'],
            ).distinct().count()
        return OrderMaster.objects.filter(
            details__state=state,
        ).distinct().count()

    @staticmethod
    def resolve_order_master(root, info, order_number=None, order_master_id=None):
        if order_number:
            return OrderMaster.objects.get(order_number=order_number)
        return OrderMaster.objects.get(pk=order_master_id)

    @staticmethod
    def resolve_order_masters(root, info, **kwargs):
        return OrderMaster.objects.all()

    @staticmethod
    def resolve_payments(root, info, **kwargs):
        return Payment.objects.all()

    @staticmethod
    def resolve_order_details(root, info, order_master_id):
        order_master = OrderMaster.objects.get(pk=order_master_id)
        order_details = order_master.details.all()
        return order_details

    @staticmethod
    def resolve_delivery(_, __, delivery_id=None, order_detail_id=None):
        if delivery_id:
            return Delivery.objects.get(pk=delivery_id)
        if order_detail_id:
            return OrderDetail.objects.get(pk=order_detail_id).delivery

    ### ta query
    my_ta_order_masters = graphene.Field(TaOrderMastersType, page=graphene.Int(), state=graphene.String(), keyword=graphene.String(), start=graphene.String(), end=graphene.String(), token=graphene.String(required=True))
    ta_order_master = graphene.Field(TaOrderMasterType, ta_order_master_id=graphene.Int())

    @staticmethod
    @login_required
    def resolve_my_ta_order_masters(_, info, token, page=1, state=None, keyword=None, start=None, end=None):
        user = info.context.user
        ta_firm = user.ta_firm
        q = Q()
        q.add(Q(ta_firm=ta_firm), q.AND)
        if keyword:
            q.add(Q(order_number=keyword) | Q(gym_name=keyword) | Q(order_master__user__name=keyword) | Q(order_master__user__phone=keyword), q.AND)
        if state and state != '전체':
            q.add(Q(state=state), q.AND)
        if start:
            start_date = datetime.strptime(end, '%Y-%m-%d').date()
            q.add(Q(date_ordered__gte=start_date), q.AND)
        if end:
            end_date = datetime.strptime(end, '%Y-%m-%d').date() + timedelta(days=1)
            q.add(Q(date_created__lte=end_date), q.AND)
        ta_order_masters = TaOrderMaster.objects.filter(q).order_by('-date_ordered')
        total_count = ta_order_masters.count()
        return TaOrderMastersType(ta_order_masters=ta_order_masters[10 * (page - 1):10 * page],
                                  total_count=total_count)
    @staticmethod
    def resolve_ta_order_master(_, __, ta_order_master_id):
        return TaOrderMaster.objects.get(pk=ta_order_master_id)

    did_use_coupon_today = graphene.Boolean()
    @staticmethod
    def resolve_did_use_coupon_today(_, info, **kwargs):
        now = datetime.now()
        today_used_coupon = Coupon.objects.filter(user=info.context.user, date_used__gte=now.date(),
                                                  date_used__lt=now.date() + timedelta(days=1))
        return True if today_used_coupon.exists() else False



class Mutation(graphene.ObjectType):
    place_order = PlaceOrder.Field()
    complete_easy_order = CompleteEasyOrder.Field()
    create_easy_order = CreateEasyOrder.Field()
    create_or_update_work = CreateOrUpdateWork.Field()
    complete_payment = CompletePayment.Field()
    assign_work = AssignWork.Field()
    change_state = ChangeState.Field()
    cancel_order = CancelOrder.Field()
    refund_order = RefundOrder.Field()
    change_order = ChangeOrder.Field()
    deposit_without_account = DepositWithoutAccount.Field()
    complete_payments_without_bank = CompletePaymentsWithoutBank.Field()
    start_shipping = StartShipping.Field()
    complete_claim = CompleteClaim.Field()
    decline_claim = DeclineClaim.Field()
    request_claim = RequestClaim.Field()
    update_work = UpdateWork.Field()
    bundle_delivery = BundleDelivery.Field()
    toggle_active = ToggleActive.Field()
    update_memo = UpdateMemo.Field()
    complete_works = CompleteWorks.Field()
    update_work_memos = UpdateWorkMemos.Field()
    ready_for_delivery = ReadyForDelivery.Field()
    complete_pre_works = CompletePreWorks.Field()
    cancel_easy_order = CancelEasyOrder.Field()
    delete_easy_order_requests = DeleteEasyOrderRequests.Field()
    pick_up = PickUp.Field()
    easy_order_to_paid = EasyOrderToPaid.Field()
    delete_order_masters = DeleteOrderMasters.Field()
    proceed_paid_orders = ProceedPaidOrders.Field()
    proceed_paid_order_details = ProceedPaidOrderDetails.Field()
    create_ta_order = CreateTaOrder.Field()
    update_ta_order = UpdateTaOrder.Field()
    me = Me.Field()
    user_cancel_order = UserCancelOrder.Field()
    save_memo = SaveMemo.Field()
    gym_order_history_by_agency = GymOrderHistoryByAgency.Field()
    order_by_smarter_money = OrderBySmarterMoney.Field()
    create_user_return_request = CreateUserReturnRequest.Field()
    create_user_change_request = CreateUserChangeRequest.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
