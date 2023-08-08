import graphene
from django.db import transaction

from cs.methods.get_order_state_detail import get_order_state_detail
from cs.models import CsRequest, ReturnRequest, ReturnRequestDetail
from cs.types.input_types.order_detail_input_type import OrderDetailInputType
from order.models import OrderDetail


class CreateReturnRequest(graphene.Mutation):
    class Arguments:
        cs_request_id = graphene.Int()
        order_details = graphene.List(OrderDetailInputType)
        return_reason = graphene.String(default_value='')
        receiver = graphene.String()
        phone = graphene.String()
        zip_code = graphene.String()
        address = graphene.String()
        detail_address = graphene.String()

        memo = graphene.String()

    success = graphene.Boolean()
    message = graphene.String()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, cs_request_id, order_details, return_reason, receiver, phone, zip_code,
               address, detail_address, **kwargs):
        try:
            for order_detail in order_details:
                old_order_detail = OrderDetail.objects.get(pk=order_detail.id)
                if old_order_detail.quantity < order_detail.quantity:
                    return CreateReturnRequest(success=False, message="{} 의 반품갯수를 {}개 이하로 설정해주세요".format(old_order_detail.product.name, old_order_detail.quantity))
                elif old_order_detail.state in ["결제완료","결제전"]:
                    return CreateReturnRequest(success=False, message="결제완료 상태인 상품은 교환, 환불 처리를 할수 없습니다. 주문변경 혹은 주문취소를 해주세요.")
            memo = kwargs.get('memo')
            cs_request = CsRequest.objects.get(pk=cs_request_id)
            order_detail_ids = [order_detail['id'] for order_detail in order_details]
            return_order_details = OrderDetail.objects.filter(pk__in=order_detail_ids)
            check_new_draft = list(set([True if return_order_detail.new_draft else False for return_order_detail in return_order_details]))
            if True in check_new_draft and return_reason == "단순변심":
                return CreateReturnRequest(success=False, message="로고시안이 있는 제품은 단순변심으로 인한 환불이 불가합니다.")
            if return_order_details.first().state == "주문취소":
                return CreateReturnRequest(success=False, message="이미 주문취소 된 상품입니다.")
            cs_request_return = ReturnRequest.objects.create(cs_request=cs_request,
                                                             return_reason=return_reason,
                                                             receiver=receiver,
                                                             phone=phone,
                                                             zip_code=zip_code,
                                                             address=address,
                                                             detail_address=detail_address,
                                                             memo=memo)
            total_products_price = 0
            for order_detail in order_details:
                old_order_detail = OrderDetail.objects.get(pk=order_detail.id)
                return_price = ((old_order_detail.product.product_master.price_gym + (old_order_detail.new_draft.price_work if old_order_detail.new_draft else 0)) * order_detail.quantity)
                total_products_price += return_price
                total_quantity = old_order_detail.quantity
                old_order_detail.quantity -= order_detail.quantity
                old_quantity = old_order_detail.quantity
                if old_quantity == 0:
                    old_order_detail.is_deleted = True
                old_order_detail.price_total -= return_price
                if old_order_detail.new_draft:
                    old_order_detail.price_work = old_order_detail.new_draft.price_work * old_order_detail.quantity
                old_order_detail.save()
                return_order_detail = old_order_detail
                return_order_detail.pk = None
                return_order_detail.quantity = order_detail.quantity
                ## 총 가격 수정 부분
                return_order_detail.price_total = return_price
                if return_order_detail.new_draft:
                    return_order_detail.price_work = return_order_detail.quantity * return_order_detail.new_draft.price_work
                return_order_detail.state = "반품요청"
                return_order_detail.is_deleted = False
                return_order_detail.save()
                ReturnRequestDetail.objects.create(cs_request_return=cs_request_return,
                                                   order_detail=return_order_detail,
                                                   price_work=return_order_detail.new_draft.price_work if return_order_detail.new_draft else 0,
                                                   return_quantity=return_order_detail.quantity,
                                                   return_price=return_price)

            cs_request_return.total_products_price = total_products_price
            cs_request_return.save()
            return CreateReturnRequest(success=True, message="반품신청이 성공적으로 완료 되었습니다.")
        except Exception as e:
            import logging
            logger = logging.getLogger('myLog')
            logger.info(e)
            return CreateReturnRequest(success=True, message="알 수 없는 에러가 발생했습니다. 개발팀 문의 바랍니다.")
