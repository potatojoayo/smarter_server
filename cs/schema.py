import graphene
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, IntegerField
from django.db.models.functions import Cast

from authentication.models import User
from business.models import Gym
from business.types import GymType
from common.models import AddressZipCode
from common.types import AddressType
from cs.methods.delivery_methods.price_delivery_method import price_delivery_method
from cs.models import CsRequest, CouponMaster, CouponIssueHistory, CouponUseHistory, CancelOrderRequest, \
    CsPartialCancelHistory, ReturnRequest, ChangeRequest, Coupon, CouponMasterIssueHistory, ChangeRequestDetail
from cs.mutations.cancel_mutations.conclude_cancel_order_without_deposit import ConcludeCancelOrderWithoutDeposit

from cs.mutations.cancel_mutations.cs_partial_cancel import CsPartialCancel
from cs.mutations.cancel_order_mutations.cancel_student import CancelStudent
from cs.mutations.change_mutations.change_student_name import ChangeStudentName
from cs.mutations.change_mutations.complete_change import CompleteChange
from cs.mutations.change_mutations.create_change_request import CreateChangeRequest
from cs.mutations.cancel_order_mutations.cs_cancel_order import CsCancelOrder
from cs.mutations.change_mutations.update_change_request import UpdateChangeRequest
from cs.mutations.coupon_mutations.create_coupon import CreateCouponMaster
from cs.mutations.coupon_mutations.issue_manual_coupon import IssueManualCoupon
from cs.mutations.coupon_mutations.update_new_member_coupon import UpdateNewMemberCoupon
from cs.mutations.coupon_mutations.update_referral_coupon import UpdateReferralCoupon
from cs.mutations.change_mutations.change_order_detail_quantity import ChangeOrderDetailQuantity
from cs.mutations.cs_request_mutations.create_cs_request import CreateCsRequest
from cs.mutations.cs_request_mutations.create_cs_request_content import CreateCsRequestContents
from cs.mutations.cs_request_mutations.create_cs_request_memo import CreateCsRequestMemo
from cs.mutations.cs_request_mutations.delete_cs_request_content import DeleteCsRequestContents
from cs.mutations.cs_request_mutations.delete_cs_request_memo import DeleteCsRequestMemo
from cs.mutations.cs_request_mutations.reply.create_content_reply import CreateContentReply
from cs.mutations.cs_request_mutations.reply.delete_content_reply import DeleteContentReply
from cs.mutations.cs_request_mutations.reply.update_content_reply import UpdateContentReply
from cs.mutations.cs_request_mutations.update_cs_request_content import UpdateCsRequestContents
from cs.mutations.cs_request_mutations.update_cs_request_state import UpdateCsRequestState
from cs.mutations.cs_request_mutations.update_cs_reuqest import UpdateCsRequest
from cs.mutations.cs_smarter_money_mutations.cs_charge_smarter_money import CsChargeSmarterMoney
from cs.mutations.cs_smarter_money_mutations.cs_subtract_smarter_money import CsSubtractSmarterMoney
from cs.mutations.order_mutations.additional_order import AdditionalOrder
from cs.mutations.return_mutations.complete_return import CompleteReturn
from cs.mutations.return_mutations.create_return_request import CreateReturnRequest
from cs.mutations.return_mutations.update_return import UpdateReturn
from cs.mutations.test import TestNumber
from cs.mutations.user_info_mutations.create_address import CreateAddress

from cs.mutations.user_info_mutations.create_or_update_user_address import CreateOrUpdateUserAddress
from cs.mutations.user_info_mutations.create_or_update_user_refund_account import CreateOrUpdateUserRefundAccount
from cs.mutations.user_info_mutations.select_address import SelectAddress
from cs.mutations.user_info_mutations.update_address import UpdateAddress
from cs.mutations.user_info_mutations.update_user_info import UpdateUserInfo
from cs.mutations.wrong_delivery import WrongDelivery
from cs.types.cancel_order_requests_type import CancelOrderRequestsType
from cs.types.change_types.change_detail_type import ChangeDetailType
from cs.types.change_types.change_info_type import ChangeInfoType
from cs.types.change_types.change_product_info_type import ChangeProductInfoType
from cs.types.change_types.change_request_type import ChangeRequestType
from cs.types.change_types.changes_type import ChangesType
from cs.types.coupon_types.coupon_info_type import CouponInfoType
from cs.types.coupon_types.coupon_master_issue_histories_type import CouponMasterIssueHistoriesType
from cs.types.coupon_types.coupon_master_type import CouponMasterType
from datetime import datetime, timedelta

from cs.types.coupon_types.coupon_masters_type import CouponMastersType
from cs.types.coupon_types.coupons_type import CouponsType
from cs.types.coupon_types.coupon_type import CouponType
from cs.types.coupon_types.issued_coupons_type import IssuedCouponsType
from cs.types.coupon_types.used_coupons_type import UsedCouponsType
from cs.types.cs_order_detail_type import CsOrderDetailType
from cs.types.cs_request_type import CsRequestType
from cs.types.cs_requests_type import CsRequestsType
from cs.types.customers_type import CustomersType
from cs.types.input_types.cs_product_input_type import CsProductInputType
from cs.types.input_types.order_detail_input_type import OrderDetailInputType
from cs.types.partial_cancel_histories_type import PartialCancelHistoriesType
from cs.types.return_types.return_info_type import ReturnInfoType
from cs.types.return_types.return_type import ReturnType
from cs.types.return_types.returns_type import ReturnsType
from order.models import OrderDetail
from order.mutations.change_order_delivery import ChangeOrderDelivery


class Query(graphene.ObjectType):

    change_detail_of_order_detail = graphene.Field(ChangeDetailType, order_detail_id=graphene.Int(required=True))

    @staticmethod
    def resolve_change_detail_of_order_detail(_, __, order_detail_id):
        order_detail = OrderDetail.objects.get(pk=order_detail_id)
        return order_detail.change_details.first()

    coupon_master_issue_histories = graphene.Field(CouponMasterIssueHistoriesType,
                                                   page=graphene.Int(),
                                                   keyword=graphene.String(),
                                                   start=graphene.String(),
                                                   end=graphene.String(),
                                                   coupon_type=graphene.String()
                                                   )

    @staticmethod
    def resolve_coupon_master_issue_histories(_, __, page, coupon_type, **kwargs):
        keyword = kwargs.get('keyword')
        start = kwargs.get('start')
        end = kwargs.get('end')
        q = Q()
        if keyword:
            q.add(Q(coupon_master__name=keyword) , q.AND)
        if start:
            date_created_start = datetime.strptime(start, '%Y-%m-%d').date()
            q.add(Q(date_issued__gte=date_created_start), q.AND)
        if end:
            date_created_end = datetime.strptime(end, '%Y-%m-%d').date() + timedelta(days=1)
            q.add(Q(date_issued__lte=date_created_end), q.AND)
        q.add(Q(coupon_master__type=coupon_type), q.AND)
        coupon_issue_histories = CouponMasterIssueHistory.objects.filter(q).order_by('-date_issued')
        return CouponMasterIssueHistoriesType(coupon_master_issue_histories=coupon_issue_histories[10 * (page - 1):10 * page],
                                 total_count=coupon_issue_histories.count())

    my_coupons = graphene.List(CouponType)

    @staticmethod
    def resolve_my_coupons(_, info):
        user: User = info.context.user
        now = datetime.now()
        return user.coupons.filter(end_of_use__gte=now).order_by('-date_used')


    # cs_requests = CsRequestField(CsRequestNode) ## 고객문의 불러오는 쿼리
    cs_requests = graphene.Field(CsRequestsType, page=graphene.Int(), category=graphene.String(),
                                 keyword=graphene.String(),
                                 cs_state=graphene.String(), start=graphene.String(), end=graphene.String())

    cs_request = graphene.Field(CsRequestType, id=graphene.Int(required=True))

    @staticmethod
    def resolve_cs_request(_, __, id):
        return CsRequest.objects.get(pk=id)

    cancel_order_requests = graphene.Field(CancelOrderRequestsType,
                                           page=graphene.Int(),
                                           state=graphene.String(),
                                           keyword=graphene.String(),
                                           start=graphene.String(),
                                           end=graphene.String(),
                                           is_without_deposit=graphene.Boolean()
                                           )

    @staticmethod
    def resolve_cancel_order_requests(_, __, page, is_without_deposit=False, state=None, keyword=None, start=None, end=None):
        q = Q(is_without_deposit=is_without_deposit)
        if keyword:
            q.add(Q(gym_name__icontains=keyword) | Q(cs_request_number__icontains=keyword) | Q(
                order_number__icontains=keyword), q.AND)
        if state and state != '전체':
            q.add(Q(state=state), q.AND)
        if start:
            start_date = datetime.strptime(start, '%Y-%m-%d').date()
            q.add(Q(date_created__gte=start_date), q.AND)
        if end:
            end_date = datetime.strptime(end, '%Y-%m-%d').date() + timedelta(days=1)
            q.add(Q(date_created__lte=end_date), q.AND)
        cancel_order_requests = CancelOrderRequest.objects.filter(q).order_by('-date_created')
        return CancelOrderRequestsType(
            cancel_order_requests=cancel_order_requests[10 * (page - 1):10 * page],
            total_count=cancel_order_requests.count()
        )

    partial_cancel_histories = graphene.Field(PartialCancelHistoriesType,
                                              page=graphene.Int(),
                                              keyword=graphene.String(),
                                              start=graphene.String(),
                                              end=graphene.String()
                                              )

    @staticmethod
    def resolve_partial_cancel_histories(_, __, page, keyword=None, start=None, end=None):
        q = Q()
        if keyword:
            q.add(Q(gym_name__icontains=keyword) | Q(cs_request_number__icontains=keyword) | Q(
                order_number__icontains=keyword), q.AND)
        if start:
            start_date = datetime.strptime(start, '%Y-%m-%d').date()
            q.add(Q(date_created__gte=start_date), q.AND)
        if end:
            end_date = datetime.strptime(end, '%Y-%m-%d').date() + timedelta(days=1)
            q.add(Q(date_created__lte=end_date), q.AND)
        partial_cancel_histories = CsPartialCancelHistory.objects.filter(q).order_by('-date_created')
        return PartialCancelHistoriesType(
            partial_cancel_histories=partial_cancel_histories[10 * (page - 1):10 * page],
            total_count=partial_cancel_histories.count()
        )

    change_request = graphene.Field(ChangeRequestType, id=graphene.Int(required=True))

    @staticmethod
    def resolve_change_request(_, __, id):
        return ChangeRequest.objects.get(pk=id)

    ## 쿠폰 발급내역
    issued_coupons = graphene.Field(IssuedCouponsType, coupon_master_id=graphene.Int(), page=graphene.Int(),
                                    coupon_type=graphene.String(),
                                    keyword=graphene.String(), start=graphene.String(), end=graphene.String())
    # 쿠폰 사용내역
    used_coupons = graphene.Field(UsedCouponsType, coupon_master_id=graphene.Int(), page=graphene.Int(),
                                  coupon_type=graphene.String(),
                                  keyword=graphene.String(), start=graphene.String(), end=graphene.String())
    coupon_master = graphene.Field(CouponMasterType, name=graphene.String())
    coupon_masters = graphene.Field(CouponMastersType, coupon_type=graphene.String(), page=graphene.Int())
    # 고객 정보 불러오기
    customers = graphene.List(GymType, keyword=graphene.String(), total_purchased_amount=graphene.Int(), prev_month_purchased_amount=graphene.Int())
    customers_with_total_count = graphene.Field(CustomersType, page=graphene.Int(),
                                                total_purchased_amount=graphene.Int(),
                                                prev_month_purchased_amount=graphene.Int(),
                                                address_zip_code_id=graphene.Int())

    @staticmethod
    def resolve_customers_with_total_count(_, __, page=None, total_purchased_amount=None, prev_month_purchased_amount=None, address_zip_code_id=None):
        q = Q()
        if total_purchased_amount:
            q.add(Q(total_purchased_amount__gte=total_purchased_amount), q.AND)
        elif prev_month_purchased_amount:
            now = datetime.now().replace(day=1)
            prev_month = now - timedelta(days=1)
            prev_month = prev_month.replace(day=1)
            q.add(Q(
                monthly_purchased_amount__date__year=prev_month.year,
                monthly_purchased_amount__date__month=prev_month.month,
                monthly_purchased_amount__amount__gte=prev_month_purchased_amount
            ), Q.AND)
        customers = Gym.objects.filter(q).order_by('-total_purchased_amount')
        if address_zip_code_id:
            address_zip_code = AddressZipCode.objects.get(pk=address_zip_code_id)
            zip_code_start = address_zip_code.zip_code_start
            zip_code_end = address_zip_code.zip_code_end
            customers = customers.filter(zip_code__isnull=False).exclude(zip_code='')
            customers = customers.annotate(zip_code_int=Cast('zip_code', output_field=IntegerField())).filter(zip_code_int__gte=int(zip_code_start),
                                                                                                    zip_code_int__lt=int(zip_code_end))

        return CustomersType(customers=customers[(page-1)*5: page*5], total_count=customers.count())



    customer = graphene.Field(GymType, id=graphene.Int())
    # 고객 주소정보
    use_address = graphene.List(AddressType, cs_request_id=graphene.Int())
    # 반품, 교환 시 배송비 계산해주는 쿼리
    calculate_delivery_price = graphene.Int(cs_request_id=graphene.Int(),
                                            order_details=graphene.List(OrderDetailInputType))

    # 수동쿠폰 발급대상 지정시 정보들
    coupon_infos = graphene.Field(CouponInfoType, coupon_master_id=graphene.Int(), subject=graphene.String(),
                                  subject_price=graphene.Int(), issue_count=graphene.Int())

    # 교환이나 반품 클릭시 order_details 가져오는 쿼리
    cs_order_details = graphene.List(CsOrderDetailType, order_detail_ids=graphene.List(graphene.Int))

    # 교환이나 반품을 클릭시 order_details 와 유저 기본 배송지 가져오는 쿼리
    refund_info = graphene.Field(ReturnInfoType, order_detail_ids=graphene.List(graphene.Int))

    @staticmethod
    def resolve_refund_info(_, __, order_detail_ids=graphene.List(graphene.Int)):
        order_details = OrderDetail.objects.filter(pk__in=order_detail_ids)
        user = order_details[0].order_master.user
        receiver = user.name
        address = user.gym.address
        detail_address = user.gym.detail_address
        zip_code = user.gym.zip_code
        return ReturnInfoType(order_details=order_details,
                              receiver=receiver,
                              address=address,
                              detail_address=detail_address,
                              zip_code=zip_code)

    # 반품 시 내부 정보들
    # refund_info = graphene.Field(RefundInfoType, cs_request_id=graphene.Int(), order_details= graphene.List(OrderDetailInputType))
    # 반품 object 불러오기
    return_request = graphene.Field(ReturnType, return_id=graphene.Int())
    return_requests = graphene.Field(ReturnsType, page=graphene.Int(), keyword=graphene.String(), state=graphene.String(),
                                     start=graphene.String(), end=graphene.String())
    @staticmethod
    def resolve_return_requests(_, __, page, keyword=None, state=None, start=None, end=None):
        q = Q()
        if keyword:
            q.add(Q(cs_request__gym__name__icontains=keyword) | Q(cs_request__request_number__icontains=keyword) | Q(
                cs_request__order_number__icontains=keyword), q.AND)
        if state and state != '전체':
            q.add(Q(state=state), q.AND)
        if start:
            start_date = datetime.strptime(start, '%Y-%m-%d').date()
            q.add(Q(date_created__gte=start_date), q.AND)
        if end:
            end_date = datetime.strptime(end, '%Y-%m-%d').date() + timedelta(days=1)
            q.add(Q(date_created__lte=end_date), q.AND)
        return_requests = ReturnRequest.objects.filter(q).order_by('-date_created')
        total_count = return_requests.count()
        return ReturnsType(return_requests=return_requests.order_by('-date_created')[10 * (page - 1):10 * page],
                           total_count=total_count)

    # 교환 시 정보들
    change_info = graphene.Field(ChangeInfoType, cs_request_id=graphene.Int(), products=graphene.List(CsProductInputType), total_changing_price=graphene.Int(),
                                 is_changed_price_exempt=graphene.Boolean(default_value=False), is_delivery_price_exempt=graphene.Boolean(default_value=False))
    # 교환 object 불러오기
    change = graphene.Field(ChangeRequestType, change_id=graphene.Int())
    change_requests = graphene.Field(ChangesType, page=graphene.Int(), keyword=graphene.String(), state=graphene.String(),
                                     start=graphene.String(), end=graphene.String())

    @staticmethod
    def resolve_change_requests(_, __, page, keyword=None, state=None, start=None, end=None):
        q = Q()
        if keyword:
            q.add(Q(cs_request__gym__name__icontains=keyword) | Q(cs_request__request_number__icontains=keyword) | Q(
                cs_request__order_number__icontains=keyword), q.AND)
        if state and state != '전체':
            q.add(Q(state=state), q.AND)
        if start:
            start_date = datetime.strptime(start, '%Y-%m-%d').date()
            q.add(Q(date_created__gte=start_date), q.AND)
        if end:
            end_date = datetime.strptime(end, '%Y-%m-%d').date() + timedelta(days=1)
            q.add(Q(date_created__lte=end_date), q.AND)
        change_requests = ChangeRequest.objects.filter(q).order_by('-date_created')
        total_count = change_requests.count()
        print(change_requests)
        print(total_count)
        return ChangesType(change_requests=change_requests.order_by('-date_created')[10 * (page - 1):10 * page],
                           total_count=total_count)
    # 교환 시 상품 정보(바뀐 상품 id, 바뀐 금액(추가금액)을 가져옴)
    changing_product_info = graphene.Field(ChangeProductInfoType, order_detail_id=graphene.Int(),
                                           quantity=graphene.Int(), color=graphene.String(), size=graphene.String())

    @staticmethod
    def resolve_changing_product_info(_, __, order_detail_id, quantity, color, size):
        order_detail = OrderDetail.objects.get(pk=order_detail_id)
        product_master = order_detail.product_master
        new_product = product_master.products.get(size=size, color=color)
        price_additional = new_product.price_additional
        if order_detail.new_draft:
            price_work = order_detail.new_draft.price_work
        else:
            price_work = 0
        changing_price = (price_additional + price_work) * quantity
        return ChangeProductInfoType(changing_product_id=new_product.id,
                                     changing_price=changing_price,
                                     price_work=price_work)

    @staticmethod
    def resolve_change_info(_, __, cs_request_id, products, total_changing_price, is_changed_price_exempt,
                            is_delivery_price_exempt):
        cs_request = CsRequest.objects.get(pk=cs_request_id)
        user = cs_request.gym.user
        total_changing_price = total_changing_price
        delivery_price_normals, delivery_price_divisions, delivery_price_individuals = price_delivery_method(
            cs_request=cs_request, products_info=products)
        total_delivery_price = max(delivery_price_normals) + sum(delivery_price_divisions) + sum(
            delivery_price_individuals)
        if is_changed_price_exempt:
            total_changing_price = 0
        if is_delivery_price_exempt:
            total_delivery_price = 0
        payment_amount = total_changing_price + total_delivery_price
        user_wallet = user.wallet
        current_smarter_money = user_wallet.balance
        after_smarter_money = current_smarter_money - payment_amount
        return ChangeInfoType(changing_products_price=total_changing_price,
                              total_delivery_price=total_delivery_price,
                              payment_amount=payment_amount,
                              current_smarter_money=current_smarter_money,
                              after_smarter_money=after_smarter_money)

    @staticmethod
    def resolve_change(_, __, change_id):
        change = ChangeRequest.objects.get(pk=change_id)
        return change

    @staticmethod
    def resolve_cs_order_details(_, __, order_detail_ids):
        return OrderDetail.objects.filter(pk__in=order_detail_ids)

    @staticmethod
    def resolve_coupon_infos(_, __, coupon_master_id, subject, subject_price, issue_count):
        coupon_master = CouponMaster.objects.get(pk=coupon_master_id)
        coupon_price = coupon_master.price
        gyms = None
        gym_ids = None
        if subject == "총 구매 금액":
            gyms = Gym.objects.filter(total_purchased_amount__gte=subject_price)
            gym_ids = gyms.values_list('id', flat=True)
        total_users_count = gyms.count()
        total_expected_price = total_users_count * issue_count * coupon_price
        return CouponInfoType(total_users_count=total_users_count,
                              total_expected_price=total_expected_price,
                              gym_ids=gym_ids)

    @staticmethod
    def resolve_user_address(_, __, cs_request_id):
        cs_request = CsRequest.objects.get(pk=cs_request_id)
        user = cs_request.gym.user
        addresses = user.addresses.filter(is_active=True)
        return addresses

    @staticmethod
    def resolve_return_request(_, __, return_id):
        return ReturnRequest.objects.get(pk=return_id)


    @staticmethod
    def resolve_calculate_delivery_price(_, __, cs_request_id, order_details):
        cs_request = CsRequest.objects.get(pk=cs_request_id)
        order_detail_objects = []
        for order_detail in order_details:
            changed_order_detail = OrderDetail.objects.get(pk=order_detail.id)
            order_detail_object = {'order_detail': changed_order_detail, 'quantity': order_detail.quantity}
            order_detail_objects.append(order_detail_object)
        delivery_price_normals, delivery_price_divisions, delivery_price_individuals = price_delivery_method(
            cs_request=cs_request, order_details=order_detail_objects)
        total_delivery_price = max(delivery_price_normals) + sum(delivery_price_divisions) + sum(
            delivery_price_individuals)
        return total_delivery_price

    @staticmethod
    def resolve_customers(_, __, keyword=None):
        q = Q()
        if keyword:
            q.add(Q(name__icontains=keyword) | Q(user__name__icontains=keyword) | Q(user__phone__icontains=keyword),
                  q.AND)
        return Gym.objects.filter(q)

    @staticmethod
    def resolve_customer(_, __, id=None):
        try:
            return Gym.objects.get(pk=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def resolve_used_coupons(_, __, page, coupon_type, **kwargs):
        coupon_masters = CouponMaster.objects.filter(type=coupon_type)
        keyword = kwargs.get('keyword')
        start = kwargs.get('start')
        end = kwargs.get('end')
        coupon_master_id = kwargs.get('coupon_master_id')
        q = Q()
        if keyword:
            q.add(Q(gym_name__icontains=keyword) | Q(coupon_number__icontains=keyword) | Q(
                order_number__icontains=keyword) | Q(coupon__referral_code__icontains=keyword), q.AND)
        if start:
            date_created_start = datetime.strptime(start, '%Y-%m-%d').date()
            q.add(Q(date_used__gte=date_created_start), q.AND)
        if end:
            date_created_end = datetime.strptime(end, '%Y-%m-%d').date() + timedelta(days=1)
            q.add(Q(date_used__lte=date_created_end), q.AND)
        q.add(Q(coupon__coupon_master__in=coupon_masters), q.AND)
        # q.add(Q(coupon__coupon_master__type=coupon_type), q.AND)
        coupon_use_histories = CouponUseHistory.objects.filter(q).order_by('-date_used')
        return UsedCouponsType(
            used_coupons_histories=coupon_use_histories[10 * (page - 1):10 * page],
            total_count=coupon_use_histories.count())

    @staticmethod
    def resolve_issued_coupons(_, __, page, coupon_type, **kwargs):
        coupon_masters = CouponMaster.objects.filter(type=coupon_type)
        keyword = kwargs.get('keyword')
        start = kwargs.get('start')
        end = kwargs.get('end')
        coupon_master_id = kwargs.get('coupon_master_id')
        q = Q()
        if keyword:
            q.add(Q(gym_name__icontains=keyword) | Q(coupon_number__icontains=keyword) | Q(coupon__referral_code__icontains=keyword), q.AND)
        if start:
            date_created_start = datetime.strptime(start, '%Y-%m-%d').date()
            q.add(Q(date_issued__gte=date_created_start), q.AND)
        if end:
            date_created_end = datetime.strptime(end, '%Y-%m-%d').date() + timedelta(days=1)
            q.add(Q(date_issued__lte=date_created_end), q.AND)
        q.add(Q(coupon__coupon_master__in=coupon_masters), q.AND)
        coupon_issue_histories = CouponIssueHistory.objects.filter(q).order_by('-date_issued')
        return IssuedCouponsType(issued_coupons_histories=coupon_issue_histories[10 * (page - 1):10 * page],
                                 total_count=coupon_issue_histories.count())

    @staticmethod
    def resolve_coupon_master(_, __, name):
        return CouponMaster.objects.filter(name=name).first()

    @staticmethod
    def resolve_coupon_masters(_, __, coupon_type, page):
        coupon_masters = CouponMaster.objects.filter(is_deleted=False, type=coupon_type).order_by('-date_created')
        return CouponMastersType(coupon_masters=coupon_masters[(page - 1) * 10: page * 10],
                                 total_count=coupon_masters.count())

    @staticmethod
    def resolve_cs_requests(_, __, page, **kwargs):
        keyword = kwargs.get('keyword')
        category = kwargs.get('category')
        cs_state = kwargs.get('cs_state')
        start = kwargs.get('start')
        end = kwargs.get('end')
        q = Q()
        if keyword:
            q.add(Q(gym__user__name__icontains=keyword) | Q(gym__name__icontains=keyword) | Q(
                gym__user__phone__icontains=keyword), q.AND)
        if category and category != '전체':
            q.add(Q(category=category), q.AND)
        if cs_state and cs_state != '전체':
            q.add(Q(cs_state=cs_state), q.AND)
        if start:
            start_date = datetime.strptime(start, '%Y-%m-%d').date()
            q.add(Q(date_requested__gte=start_date), q.AND)
        if end:
            end_date = datetime.strptime(end, '%Y-%m-%d').date() + timedelta(days=1)
            q.add(Q(date_requested__lte=end_date), q.AND)
        q.add(Q(is_deleted=False), q.AND)
        cs_requests = CsRequest.objects.filter(q).order_by('-date_requested')
        return CsRequestsType(
            cs_requests=cs_requests[10 * (page - 1):10 * page],
            total_count=cs_requests.count()
        )


class Mutation(graphene.ObjectType):
    test_number = TestNumber.Field()
    create_cs_request = CreateCsRequest.Field()
    update_cs_request = UpdateCsRequest.Field()
    create_cs_request_contents = CreateCsRequestContents.Field()
    update_cs_request_contents = UpdateCsRequestContents.Field()
    delete_cs_request_contents = DeleteCsRequestContents.Field()
    create_cs_request_memo = CreateCsRequestMemo.Field()
    delete_cs_request_memo = DeleteCsRequestMemo.Field()
    update_user_info = UpdateUserInfo.Field()
    create_or_update_user_address = CreateOrUpdateUserAddress.Field()
    create_or_update_user_refund_account = CreateOrUpdateUserRefundAccount.Field()
    update_referral_coupon = UpdateReferralCoupon.Field()
    update_new_member_coupon = UpdateNewMemberCoupon.Field()
    update_cs_request_state = UpdateCsRequestState.Field()
    update_address = UpdateAddress.Field()
    create_coupon = CreateCouponMaster.Field()
    create_address = CreateAddress.Field()
    cs_charge_smarter_money = CsChargeSmarterMoney.Field()
    cs_subtract_smarter_money = CsSubtractSmarterMoney.Field()
    issue_manual_coupon = IssueManualCoupon.Field()
    create_change_request = CreateChangeRequest.Field()
    cs_cancel_order = CsCancelOrder.Field()
    change_order_detail_quantity = ChangeOrderDetailQuantity.Field()
    cs_partial_cancel = CsPartialCancel.Field()
    create_return_request = CreateReturnRequest.Field()
    additional_order = AdditionalOrder.Field()
    conclude_cancel_order_without_deposit = ConcludeCancelOrderWithoutDeposit.Field()
    update_change_request = UpdateChangeRequest.Field()
    complete_change = CompleteChange.Field()
    update_return = UpdateReturn.Field()
    complete_return = CompleteReturn.Field()
    select_address = SelectAddress.Field()
    wrong_delivery = WrongDelivery.Field()
    create_content_reply = CreateContentReply.Field()
    delete_content_reply = DeleteContentReply.Field()
    update_content_reply = UpdateContentReply.Field()
    cancel_student = CancelStudent.Field()
    change_student_name = ChangeStudentName.Field()
    change_order_delivery = ChangeOrderDelivery.Field()
schema = graphene.Schema(query=Query, mutation=Mutation)
