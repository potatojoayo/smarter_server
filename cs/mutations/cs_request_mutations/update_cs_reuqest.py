import graphene
from django.utils import timezone

from cs.models import CsRequest
from order.models import OrderMaster


class UpdateCsRequest(graphene.Mutation):
    class Arguments:
        cs_request_id = graphene.Int()
        category = graphene.String()
        reason = graphene.String()
        memo = graphene.String()
        cs_state = graphene.String()
        order_master_id = graphene.Int()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, cs_request_id, **kwargs):
        try:
            cs_request = CsRequest.objects.get(pk=cs_request_id)
            category = kwargs.get('category')
            reason = kwargs.get('reason')
            memo = kwargs.get('memo')
            cs_state = kwargs.get('cs_state')
            order_master_id = kwargs.get('order_master_id')
            if order_master_id:
                order_master = OrderMaster.objects.get(pk=order_master_id)
                order_state = '결제전'
                order_number = order_master.order_number
                if order_master.details.filter(state__icontains="배송"):
                    order_state = "배송"
                elif order_master.details.filter(state__icontains="작업"):
                    order_state = "작업"
                elif order_master.details.filter(state__icontains="결제완료"):
                    order_state = "결제완료"
                cs_request.order_master_id = order_master_id
                cs_request.order_state = order_state
                cs_request.order_number = order_number
            if category:
                cs_request.category = category
            elif reason:
                cs_request.reason = reason
            elif memo:
                cs_request.memo = memo
            elif cs_state:
                if cs_state == '처리완료':
                    cs_request.date_completed = timezone.now()
                cs_request.cs_state = cs_state
            cs_request.save()

            return UpdateCsRequest(success=True)
        except:
            import logging
            logger = logging.getLogger('myLog')
            logger.info(e)
            return UpdateCsRequest(success=False)
