import graphene
from django.db import transaction

from cs.methods.get_order_state import get_order_state
from cs.methods.get_order_state_detail import get_order_state_detail
from cs.models import ChangeRequest, ChangeRequestDetail
from cs.types.input_types.change_input_type import ChangeInputType
from order.models import OrderDetail
from product.models import Product
from server.settings import logger


class CreateUserChangeRequest(graphene.Mutation):
    class Arguments:
        order_detail_id = graphene.Int()
        changing_product_id = graphene.Int()
        changing_quantity = graphene.Int()
        change_reason = graphene.String(default_value='')
        pick_up_receiver = graphene.String()
        pick_up_phone = graphene.String()
        pick_up_address = graphene.String()
        pick_up_detail_address = graphene.String()
        pick_up_zip_code = graphene.String()
        delivery_receiver = graphene.String()
        delivery_phone = graphene.String()
        delivery_address = graphene.String()
        delivery_zip_code = graphene.String()
        delivery_detail_address = graphene.String()
        memo = graphene.String()

    success = graphene.Boolean()
    message = graphene.String()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, info, order_detail_id, changing_product_id,  changing_quantity, change_reason,   **kwargs):
        try:
            order_detail = OrderDetail.objects.get(pk=order_detail_id)
            order_state = get_order_state(order_master=order_detail.order_master)
            if '배송' not in order_state:
                return CreateUserChangeRequest(success=False, message="배송이후인 상품들에 대해서만 교환진행이 가능합니다.")
            # check_new_draft = list(set([True if change_order_detail.new_draft else False for change_order_detail in
            # change_order_details])) if True in check_new_draft and change_reason == "단순변심": return
            # CreateUserChangeRequest(success=False, message="로고시안이 있는 제품은 단순변심으로 인한 교환이 불가합니다.")
            if order_detail.state == '주문취소':
                return CreateUserChangeRequest(success=False, message="이미 주문취소 된 제품입니다.")
            change_request = ChangeRequest.objects.create(user=info.context.user, change_reason=change_reason,  **kwargs)
            total_changing_price = 0
            changed_product = order_detail.product
            price_work = order_detail.new_draft.price_work if order_detail.new_draft else 0
            changing_product = Product.objects.get(pk=changing_product_id)
            changed_price_additional = changed_product.price_additional
            changing_price_additional = changing_product.price_additional
            changing_price = changing_price_additional - changed_price_additional
            total_detail_changing_price = changing_price * changing_quantity
            order_detail.quantity -= changing_quantity
            if order_detail.quantity == 0:
                order_detail.is_deleted = True
            order_detail.save()

            old_change_order_detail = OrderDetail.objects.filter(order_detail_number=order_detail.order_detail_number, state="교환요청")
            if old_change_order_detail.exists():
                order_detail = old_change_order_detail.first()
                order_detail.quantity += changing_quantity
                order_detail.price_total += total_detail_changing_price
                order_detail.save()
            else:
                order_detail.pk = None
                order_detail.quantity = changing_quantity
                # 총 가격 수정 부분
                order_detail.price_total = total_detail_changing_price
                order_detail.state = "교환요청"
                order_detail.is_deleted = False
                order_detail.save()
            ChangeRequestDetail.objects.create(cs_request_change=change_request,
                                               changed_product=changed_product,
                                               changing_product=changing_product,
                                               price_work=price_work,
                                               changing_price=changing_price,
                                               changing_quantity=changing_quantity,
                                               total_changing_price=total_detail_changing_price,
                                               order_detail=order_detail)
            total_changing_price += total_detail_changing_price
            change_request.total_changing_price = total_changing_price
            change_request.price_to_pay = total_changing_price
            change_request.save()
            return CreateUserChangeRequest(success=True, message="교환 요청이 성공적으로 완료 되었습니다.")
        except Exception as e:
            logger.info('create_user_change_request_error')
            logger.info(e)
            return CreateUserChangeRequest(success=False, message="오류가 발생하였습니다.")