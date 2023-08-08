import graphene
from django.db import transaction
from django.db.models import Q

from cs.methods.check_quantity_methods.check_change_quantity import check_change_quantity
from cs.models import ChangeRequest, ChangeRequestDetail
from cs.types.input_types.change_detail_input_type import ChangeDetailInputType
from order.models import Delivery, OrderDetail
from product.models import Product


class UpdateChangeRequest(graphene.Mutation):
    class Arguments:
        change_request_id = graphene.Int()
        change_request_details = graphene.List(ChangeDetailInputType)
        change_reason = graphene.String()
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
        is_changed_price_exempt = graphene.Boolean()
        delivery_price = graphene.Int()
        is_delivery_price_exempt = graphene.Boolean()
        memo = graphene.String()
        delivery_agency_id = graphene.Int()
        tracking_number = graphene.String()

    success = graphene.Boolean()
    message = graphene.String()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, **kwargs):
        try:
            input_change_details = kwargs.pop('change_request_details')
            is_normal, message = check_change_quantity(change_details=input_change_details)
            if is_normal is False :
                return UpdateChangeRequest(success=False, message=message)
            change_request_id = kwargs.pop('change_request_id')
            delivery_agency_id = kwargs.pop('delivery_agency_id') if 'delivery_agency_id' in kwargs.keys() else None
            tracking_number = kwargs.pop('tracking_number') if 'tracking_number' in kwargs.keys() else None
            ChangeRequest.objects.filter(pk=change_request_id).update(**kwargs)
            change_request = ChangeRequest.objects.get(pk=change_request_id)
            if delivery_agency_id and tracking_number:
                if not change_request.delivery:
                    change_request.delivery = Delivery.objects.create(delivery_agency_id=delivery_agency_id, tracking_number=tracking_number)
                    change_request.save()
                else:
                    change_request.delivery.delivery_agency_id=delivery_agency_id
                    change_request.delivery.tracking_number=tracking_number
                    change_request.delivery.save()
            total_changing_price = 0
            for input_change_detail in input_change_details:
                change_detail = ChangeRequestDetail.objects.get(pk=input_change_detail.id)
                changing_product = Product.objects.get(pk=input_change_detail.changing_product_id)
                change_gap = change_detail.order_detail.quantity - input_change_detail.changing_quantity
                if change_gap != 0:
                    order_detail_number = change_detail.order_detail.order_detail_number
                    q = Q()
                    q.add(Q(state__in="교환") | Q(state__in="반품"), q.AND)
                    old_order_detail = OrderDetail.objects.filter(order_detail_number=order_detail_number).exclude(q).first()
                    print(old_order_detail.id)
                    old_order_detail_quantity = old_order_detail.quantity
                    new_order_detail_quantity = old_order_detail_quantity + change_gap
                    old_order_detail.quantity = new_order_detail_quantity
                    if new_order_detail_quantity == 0:
                        old_order_detail.is_deleted = True
                    else:
                        old_order_detail.is_deleted = False
                    old_order_detail.save()
                    change_detail.order_detail.quantity = input_change_detail.changing_quantity
                    ## 총 가격 수정 부분
                    change_detail.order_detail.price_total = new_order_detail_quantity * old_order_detail.product.product_master.price_gym
                    change_detail.order_detail.save()
                change_detail.changing_product = changing_product
                change_detail.changing_price = changing_product.price_additional - change_detail.changed_product.price_additional
                change_detail.changing_quantity = input_change_detail.changing_quantity
                change_detail.total_changing_price = change_detail.changing_price * change_detail.changing_quantity
                total_changing_price += change_detail.changing_price * change_detail.changing_quantity
                change_detail.save()
                change_detail.order_detail.save()
                change_detail.order_detail.quantity = input_change_detail.changing_quantity
            change_request.total_changing_price = total_changing_price
            is_change_price_exempt = kwargs.get('is_change_price_exempt')
            payment_amount = 0 if is_change_price_exempt else total_changing_price
            delivery_price = kwargs.get('delivery_price')
            is_delivery_price_exempt = kwargs.get('is_delivery_price_exempt')
            change_request.delivery_price = delivery_price
            payment_amount += 0 if is_delivery_price_exempt else delivery_price

            user_wallet = change_request.cs_request.gym.user.wallet
            current_smarter_money = user_wallet.balance
            after_smarter_money = current_smarter_money - payment_amount
            change_request.current_smarter_money = current_smarter_money
            change_request.after_smarter_money = after_smarter_money
            change_request.save()

            return UpdateChangeRequest(success=True, message="교환정보가 수정되었습니다.")
        except Exception as e:
            print(e)
            import logging
            logger = logging.getLogger('myLog')
            logger.info(e)
            return UpdateChangeRequest(success=False, message="알 수 없는 에러가 발생했습니다. 개발팀 문의 바랍니다.")

