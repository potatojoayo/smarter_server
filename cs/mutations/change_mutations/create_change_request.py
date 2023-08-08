from datetime import datetime

import graphene
from django.db import transaction
from django.db.models import Q

from cs.models import CsRequest, ChangeRequestDetail, ChangeRequest
from cs.types.input_types.change_input_type import ChangeInputType
from order.models import OrderDetail
from product.models import Product


class CreateChangeRequest(graphene.Mutation):
    class Arguments:
        cs_request_id = graphene.Int(required=True)
        order_details = graphene.List(ChangeInputType)
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
    def mutate(cls, _, __, **kwargs):
        try:
            cs_request_id = kwargs.get('cs_request_id')
            input_order_details = kwargs.get('order_details')
            change_reason = kwargs.get('change_reason')
            pick_up_receiver = kwargs.get('pick_up_receiver')
            pick_up_phone = kwargs.get('pick_up_phone')
            pick_up_address = kwargs.get('pick_up_address')
            pick_up_detail_address = kwargs.get('pick_up_detail_address')
            pick_up_zip_code = kwargs.get('pick_up_zip_code')
            delivery_receiver = kwargs.get('delivery_receiver')
            delivery_phone = kwargs.get('delivery_phone')
            delivery_address = kwargs.get('delivery_address')
            delivery_detail_address = kwargs.get('delivery_detail_address')
            delivery_zip_code = kwargs.get('delivery_zip_code')
            memo = kwargs.get('memo')
            for input_order_detail in input_order_details:
                old_order_detail = OrderDetail.objects.get(pk=input_order_detail.order_detail_id)
                if old_order_detail.quantity < input_order_detail.changing_quantity:
                    return CreateChangeRequest(success=False, message="{} 의 교환갯수를 {}개 이하로 설정해주세요.".format(old_order_detail.product.name, old_order_detail.quantity))
                elif old_order_detail.state in ["결제완료","결제전"]:
                    return CreateChangeRequest(success=False, message="결제완료 상태인 상품은 교환, 환불 처리를 할수 없습니다. 주문변경 혹은 주문취소를 해주세요.")
            cs_request = CsRequest.objects.get(pk=cs_request_id)
            change_request = ChangeRequest.objects.create(cs_request=cs_request,
                                                             change_reason=change_reason,
                                                             pick_up_receiver=pick_up_receiver,
                                                             pick_up_phone=pick_up_phone,
                                                             pick_up_address=pick_up_address,
                                                             pick_up_detail_address=pick_up_detail_address,
                                                             pick_up_zip_code=pick_up_zip_code,
                                                             delivery_receiver=delivery_receiver,
                                                             delivery_phone=delivery_phone,
                                                             delivery_address=delivery_address,
                                                             delivery_detail_address=delivery_detail_address,
                                                             delivery_zip_code=delivery_zip_code,
                                                             memo=memo)
            total_changing_price = 0
            for input_order_detail in input_order_details:
                old_order_detail = OrderDetail.objects.get(pk=input_order_detail.order_detail_id)
                changed_product = old_order_detail.product
                price_work = old_order_detail.new_draft.price_work if old_order_detail.new_draft else 0
                changing_product = Product.objects.get(pk=input_order_detail.changing_product_id)
                changed_price_additional = changed_product.price_additional
                changing_price_additional = changing_product.price_additional
                changing_price = changing_price_additional - changed_price_additional + price_work
                total_detail_changing_price = changing_price * input_order_detail.changing_quantity
                old_order_detail.price_option = total_detail_changing_price
                old_order_detail.quantity -= input_order_detail.changing_quantity
                # old_order_detail.price_total -= total_detail_changing_price
                old_quantity = old_order_detail.quantity
                old_order_detail.price_option = changed_price_additional * old_quantity
                if old_quantity== 0:
                    old_order_detail.is_deleted = True
                if old_order_detail.new_draft:
                    old_order_detail.price_work = old_order_detail.new_draft.price_work * old_order_detail.quantity
                old_order_detail.price_total = ((old_order_detail.product.product_master.price_gym + (old_order_detail.new_draft.price_work if old_order_detail.new_draft else 0)) * old_quantity)
                old_order_detail.save()
                change_order_detail = old_order_detail
                change_order_detail.pk = None
                change_order_detail.quantity = input_order_detail.changing_quantity
                ## 총 가격 수정 부분
                change_order_detail.state = "교환요청"
                change_order_detail.is_deleted = False
                change_order_detail.price_total = ((change_order_detail.product.product_master.price_gym + (change_order_detail.new_draft.price_work if change_order_detail.new_draft else 0)) * input_order_detail.changing_quantity)
                if change_order_detail.new_draft:
                    change_order_detail.price_work = change_order_detail.quantity * change_order_detail.new_draft.price_work
                change_order_detail.save()
                ChangeRequestDetail.objects.create(cs_request_change=change_request,
                                                   changed_product=changed_product,
                                                   changing_product=changing_product,
                                                   price_work=price_work,
                                                   changing_price=changing_price,
                                                   changing_quantity=input_order_detail.changing_quantity,
                                                   total_changing_price=total_detail_changing_price,
                                                   order_detail=change_order_detail)

                total_changing_price += total_detail_changing_price

            change_request.total_changing_price = total_changing_price
            change_request.price_to_pay = total_changing_price
            change_request.save()
            return CreateChangeRequest(success=True, message="교환신청이 성공적으로 완료 되었습니다.")
        except Exception as e:
            print(e)
            import logging
            logger = logging.getLogger('myLog')
            logger.info(e)
            return CreateChangeRequest(success=False, message="알 수 없는 에러가 발생했습니다. 개발팀 문의 바랍니다.")
