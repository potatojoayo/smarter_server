import graphene
from django.db import transaction
from django.db.models import Q

from cs.methods.check_quantity_methods.check_return_quantity import check_return_quantity
from cs.models import ReturnRequest, ReturnRequestDetail
from cs.types.input_types.refund_detail_input_type import ReturnDetailInputType
from order.models import OrderDetail


class UpdateReturn(graphene.Mutation):
    class Arguments:
        return_id = graphene.Int()
        return_details = graphene.List(ReturnDetailInputType)
        return_reason = graphene.String()
        receiver = graphene.String()
        phone = graphene.String()
        zip_code = graphene.String()
        address = graphene.String()
        detail_address = graphene.String()
        delivery_price = graphene.Int()
        is_delivery_price_exempt = graphene.Boolean()
        memo = graphene.String()

    success = graphene.Boolean()
    message = graphene.String()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, **kwargs):
        try:
            return_id = kwargs.pop('return_id')
            input_return_details = kwargs.pop('return_details')
            is_normal, message = check_return_quantity(return_details=input_return_details) ## 반품개수 초과시 걸러주는 메소드
            if is_normal is False:
                return UpdateReturn(success=False, message=message)
            total_products_price = 0
            for input_return_detail in input_return_details:
                return_detail = ReturnRequestDetail.objects.get(pk=input_return_detail.id)
                return_gap = return_detail.return_quantity - input_return_detail.return_quantity
                price_work = return_detail.order_detail.new_draft.price_work if return_detail.order_detail.new_draft else 0
                if return_gap != 0:
                    order_detail_number = return_detail.order_detail.order_detail_number
                    q = Q()
                    q.add(Q(state__in="교환") | Q(state__in="반품"), q.AND)
                    old_order_detail = OrderDetail.objects.filter(order_detail_number=order_detail_number).exclude(q).first()
                    old_order_detail_quantity = old_order_detail.quantity
                    new_order_detail_quantity = old_order_detail_quantity + return_gap
                    old_order_detail.quantity = new_order_detail_quantity
                    if new_order_detail_quantity == 0 :
                        old_order_detail.is_deleted = True
                    else:
                        old_order_detail.is_deleted = False
                    old_order_detail.save()
                    return_detail.return_quantity = input_return_detail.return_quantity
                    total_products_price += (return_detail.order_detail.product_master.price_gym+price_work) * input_return_detail.return_quantity
                    return_detail.save()
                    return_detail.order_detail.quantity = input_return_detail.return_quantity
                    ## 총 가격 수정 부분
                    return_detail.order_detail.price_total = (return_detail.order_detail.product_master.price_gym+price_work) * input_return_detail.return_quantity
                    return_detail.order_detail.save()
                else:
                    total_products_price += (return_detail.order_detail.product_master.price_gym + price_work) * return_detail.return_quantity
            ReturnRequest.objects.filter(pk=return_id).update(**kwargs)
            return_request = ReturnRequest.objects.get(pk=return_id)
            return_request.total_products_price = total_products_price
            return_request.total_return_price = total_products_price if return_request.is_delivery_price_exempt else total_products_price + return_request.delivery_price
            return_request.save()
            return UpdateReturn(success=True, message="반품정보가 성공적으로 저장되었습니다.")
        except Exception as e:
            import logging
            logger = logging.getLogger('myLog')
            logger.info(e)
            return UpdateReturn(success=False, message="오류가 발생하였습니다. 개발팀에 문의해주세요")

