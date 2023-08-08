import graphene
from django.db import transaction
from django.db.models import Q

from cs.methods.check_quantity_methods.check_return_quantity import check_return_quantity
from cs.models import ReturnRequest, CsPartialCancelHistory, ReturnRequestDetail
from cs.types.input_types.refund_detail_input_type import ReturnDetailInputType
from order.models import OrderDetail
from smarter_money.models import SmarterMoneyHistory, SmarterPaidHistory
from datetime import datetime

class CompleteReturn(graphene.Mutation):
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
            is_normal , message = check_return_quantity(return_details=input_return_details)
            if is_normal is False:
                return CompleteReturn(success=False, message=message)
            ReturnRequest.objects.filter(pk=return_id).update(**kwargs)
            return_request = ReturnRequest.objects.get(pk=return_id)
            total_products_price = 0
            for input_return_detail in input_return_details:
                return_detail = ReturnRequestDetail.objects.get(pk=input_return_detail.id)
                return_order_detail = return_detail.order_detail
                return_order_detail.state = '반품완료'
                ## 현재 return_quantity 와 이전 return_quantity의 차이
                return_gap = return_detail.return_quantity - input_return_detail.return_quantity
                price_work = return_detail.order_detail.new_draft.price_work if return_detail.order_detail.new_draft else 0
                # 바뀐 반품 최종금액
                result_return_price = (return_detail.order_detail.product_master.price_gym + price_work) * input_return_detail.return_quantity
                # 변동되는 금액
                gap_return_price = (return_detail.order_detail.product_master.price_gym + price_work) * return_gap
                if return_gap != 0 :
                    total_products_price += result_return_price
                    order_detail_number = return_detail.order_detail.order_detail_number
                    q = Q()
                    q.add(Q(state__in="교환") | Q(state__in="반품"), q.AND)
                    old_order_detail = OrderDetail.objects.filter(order_detail_number=order_detail_number).exclude(q).first()
                    old_order_detail_quantity = old_order_detail.quantity
                    new_order_detail_quantity = old_order_detail_quantity + return_gap
                    old_order_detail.quantity = new_order_detail_quantity
                    old_order_detail.price_total += gap_return_price
                    if new_order_detail_quantity == 0 :
                        old_order_detail.is_deleted = True
                    else:
                        old_order_detail.is_deleted = False
                    old_order_detail.save()
                    return_detail.return_quantity = input_return_detail.return_quantity
                    return_order_detail.quantity = input_return_detail.return_quantity
                    return_order_detail.price_total = result_return_price
                else:
                    total_products_price += (return_detail.order_detail.product_master.price_gym + price_work) * return_detail.return_quantity

                return_detail.save()
                return_order_detail.save()
            return_request.total_products_price = total_products_price
            delivery_price = kwargs.get('delivery_price')
            is_delivery_price_exempt = kwargs.get('is_delivery_price_exempt')
            delivery_price = 0 if is_delivery_price_exempt else delivery_price
            if is_delivery_price_exempt and delivery_price > 0 :
                SmarterPaidHistory.objects.create(return_request=return_request, amount=delivery_price, reason="반품배송금액 지불")
            return_request.total_return_price = total_products_price - delivery_price
            user_wallet = return_request.cs_request.gym.user.wallet if return_request.cs_request else return_request.user.wallet
            current_smarter_money = user_wallet.balance
            after_smarter_money = current_smarter_money  + total_products_price - delivery_price
            return_request.current_smarter_money = current_smarter_money
            return_request.after_smarter_money = after_smarter_money
            return_request.state = "반품완료"
            return_request.save()
            user_wallet.balance = after_smarter_money
            user_wallet.save()
            if total_products_price - delivery_price != 0:
                order_master = return_request.cs_request.order_master if return_request.cs_request else return_request.return_details.all().first().order_detail.order_master
                user = return_request.cs_request.gym.user if return_request.cs_request else return_request.user
                SmarterMoneyHistory.objects.create(
                    order_master=order_master,
                    history_number='R{}{}'.format(user.phone, datetime.now().strftime('%y%m%d%H%M%S')),
                    wallet=user.wallet,
                    transaction_type='적립' ,
                    amount=total_products_price - delivery_price,
                    description='반품적립')
            return CompleteReturn(success=True, message="반품이 성공적으로 완료되었습니다.")
        except Exception as e:
            import logging
            logger = logging.getLogger('myLog')
            logger.info(e)
            return CompleteReturn(success=False, message="오류가 발생하였습니다. 개발팀에 문의해주세요.")


