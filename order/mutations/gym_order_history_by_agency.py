from datetime import datetime, timedelta

import graphene

from order.models import OrderMaster
from order.types.gym_order_history_by_agency_type import GymOrderHistoryByAgencyType


class GymOrderHistoryByAgency(graphene.Mutation):
    class Arguments:
        date_from = graphene.Date()
        date_to = graphene.Date()
        agency_name = graphene.String()

    gym_order_history_by_agency = graphene.List(GymOrderHistoryByAgencyType)

    @classmethod
    def mutate(cls, _, __, date_from, date_to, agency_name=None):
        date_to = date_to + timedelta(days=1)
        if agency_name:
            order_masters = OrderMaster.objects.filter(date_created__gte=date_from.strftime('%Y-%m-%d'), date_created__lte=date_to.strftime('%Y-%m-%d'), user__gym__agency__name=agency_name)
        else:
            order_masters = OrderMaster.objects.filter(date_created__gte=date_from.strftime('%Y-%m-%d'), date_created__lte=date_to.strftime('%Y-%m-%d'))
        histories = []
        for order_master in order_masters:
            for order_detail in order_master.details.all():
                histories.append(GymOrderHistoryByAgencyType(user_name=order_master.user.name,
                                                             gym_name=order_master.user.gym.name,
                                                             agency_name=order_master.user.gym.agency.name if order_master.user.gym.agency else None,
                                                             date_created=order_master.date_created,
                                                             price_gym=order_detail.price_gym,
                                                             quantity=order_detail.quantity,
                                                             price_total=order_detail.price_total,
                                                             ))
        return GymOrderHistoryByAgency(gym_order_history_by_agency=histories)





