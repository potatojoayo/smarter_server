import graphene
from django.db import transaction
from datetime import datetime

from business.models import Gym
from cs.methods.get_order_state import get_order_state
from cs.models import CsRequest, CsRequestContents, CsRequestMemos
from order.models import OrderMaster


class CreateCsRequest(graphene.Mutation):
    class Arguments:
        order_master_id = graphene.Int()
        gym_id = graphene.Int(required=True)
        category = graphene.String(required=True)
        reason = graphene.String()
        contents = graphene.String()
        memo = graphene.String()

    success = graphene.String()
    cs_request_id = graphene.Int()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, gym_id, category, reason=None, contents=None, memo=None, order_master_id=None):
        order_master = None
        order_state = None
        order_number = None
        if order_master_id:
            order_master = OrderMaster.objects.get(pk=order_master_id)
            order_number = order_master.order_number
            order_state = get_order_state(order_master)

        gym = Gym.objects.get(pk=gym_id)

        try:
            now = datetime.now()
            request_number = 'R'+str(now.year)[2:4] + \
                             str(now.month).rjust(2, '0') + \
                             str(now.day).rjust(2, '0') + \
                             str(now.hour).rjust(2, '0') + \
                             str(now.minute).rjust(2, '0') + \
                             str(now.second).rjust(2, '0') + \
                             str(gym.id % 100).rjust(2, '0')

            cs_request = CsRequest.objects.create(
                request_number=request_number,
                order_master=order_master,
                gym=gym,
                category=category,
                order_state=order_state,
                reason=reason,
                order_number=order_number
            )
            if contents:
                CsRequestContents.objects.create(cs_request=cs_request,
                                                 contents=contents)
            if memo:
                CsRequestMemos.objects.create(cs_request=cs_request,
                                              contents=memo)
            return CreateCsRequest(success=True, cs_request_id=cs_request.id)
        except Exception as e :
            import logging
            logger = logging.getLogger('myLog')
            logger.info(e)
            return CreateCsRequest(success=False)

