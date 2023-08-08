import graphene
from django.db import transaction

from cs.methods.get_order_state import get_order_state
from cs.models import ReturnRequest, ReturnRequestDetail
from order.models import OrderDetail
from server.settings import logger


class CreateUserReturnRequest(graphene.Mutation):
    class Arguments:
        order_detail_id = graphene.Int(required=True)
        quantity = graphene.Int(required=True)
        return_reason = graphene.String()
        receiver = graphene.String()
        phone = graphene.String()
        zip_code = graphene.String()
        address = graphene.String()
        detail_address = graphene.String()

    success = graphene.Boolean()
    message = graphene.String()
    @classmethod
    @transaction.atomic()
    def mutate(cls, _, info, order_detail_id, quantity, receiver, phone, zip_code, address, detail_address, return_reason=None):
        try:
            user = info.context.user
            order_detail = OrderDetail.objects.get(pk=order_detail_id)
            order_state = get_order_state(order_detail.order_master)
            if '배송' not in order_state:
                return CreateUserReturnRequest(success=False, message="배송이후인 상품들에 대해서만 환불진행을 할수 있습니다.")
            # if order_detail.new_draft:
            #     return CreateUserReturnRequest(success=False, message="로고시안이 있는 제품은 단순변심으로 인한 환불이 불가합니다.")
            if order_detail.state == "주문취소":
                return CreateUserReturnRequest(success=False, message="이미 주문취소 된 상품입니다.")

            return_request = ReturnRequest.objects.create(user=user,
                                                            return_reason=return_reason,
                                                             receiver=receiver,
                                                             phone=phone,
                                                             zip_code=zip_code,
                                                             address=address,
                                                             detail_address=detail_address,
                                                             memo='')
            total_products_price = 0

            old_order_detail = OrderDetail.objects.get(pk=order_detail.id)
            return_price = ((old_order_detail.product.product_master.price_gym + (old_order_detail.new_draft.price_work if old_order_detail.new_draft else 0)) * quantity)
            old_cancel_order_detail = OrderDetail.objects.filter(order_detail_number=old_order_detail.order_detail_number, state="반품요청")
            total_products_price += return_price
            old_order_detail.quantity -= quantity
            old_quantity = old_order_detail.quantity
            if old_quantity == 0:
                old_order_detail.is_deleted = True
            old_order_detail.save()
            if old_cancel_order_detail.exists():
                return_order_detail = old_cancel_order_detail.first()
                return_order_detail.quantity += quantity
                return_order_detail.price_total += return_price
                return_order_detail.save()
            else:
                return_order_detail = old_order_detail
                return_order_detail.pk = None
                return_order_detail.quantity = quantity
                ## 총 가격 수정 부분
                return_order_detail.price_total = return_price
                return_order_detail.state = "반품요청"
                return_order_detail.is_deleted = False
                return_order_detail.save()
            ReturnRequestDetail.objects.create(cs_request_return=return_request,
                                               order_detail=return_order_detail,
                                               price_work=order_detail.new_draft.price_work if order_detail.new_draft else 0,
                                               return_quantity=order_detail.quantity,
                                               return_price=return_price,
                                               )

            return_request.total_products_price = total_products_price
            return_request.save()
            return CreateUserReturnRequest(success=True, message="반품신청이 완료되었습니다.")
        except Exception as e:
            logger.info('create_user_return_request_error')
            logger.info('order_detail_id : '+str(order_detail_id))
            logger.info('quantity : '+str(quantity))
            logger.info(e)
            return CreateUserReturnRequest(success=False, message="오류가 발생하였습니다.")




