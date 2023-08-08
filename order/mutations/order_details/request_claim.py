import graphene
from django.contrib.auth.models import Group
from django.db import transaction

from authentication.models import User
from common.methods.create_notification import create_notification
from common.methods.send_notification import send_notification
from common.models import Notification
from order.models import Claim, OrderDetail


class RequestClaim(graphene.Mutation):
    class Arguments:
        order_detail_id = graphene.Int()
        quantity = graphene.Int()
        reason = graphene.String()
        type = graphene.String()

    success = graphene.Boolean()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, info, order_detail_id, quantity, reason, type):
        user = info.context.user
        order_detail = OrderDetail.objects.get(pk=order_detail_id)
        product = order_detail.product
        product_master = product.product_master
        price_work = 0
        price_work_labor = 0
        draft = order_detail.draft
        if draft:
            price_work = draft.price_work
            price_work_labor = draft.price_work_labor

        Claim.objects.create(order_detail_id=order_detail_id,
                             user=user,
                             quantity=quantity,
                             price_products=product_master.price_gym * quantity,
                             price_total_work=price_work * quantity,
                             price_total_work_labor= price_work_labor * quantity,
                             price_total=(product_master.price_gym + price_work )*quantity,
                             reason=reason,
                             state='{}요청'.format(type)
                             )
        #send_notification(user=user, type='{}요청'.format(type), product_names=product.name, quantity=quantity)
    
        return RequestClaim(success=True)

