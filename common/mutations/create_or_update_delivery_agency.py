import graphene

from common.models import DeliveryAgency
from common.types.delivery_agency_input_type import DeliveryAgencyInputType


class CreateOrUpdateDeliveryAgency(graphene.Mutation):
    class Arguments:
        delivery_agencies = graphene.List(DeliveryAgencyInputType)
        deleted_agency_ids = graphene.List(graphene.Int)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, delivery_agencies, deleted_agency_ids):
        for agency in delivery_agencies:
            if agency.id:
                DeliveryAgency.objects.filter(pk=agency.id).update(**agency)

            else:
                DeliveryAgency.objects.create(**agency)

        for id in deleted_agency_ids:
            DeliveryAgency.objects.filter(pk=id).delete()

        return CreateOrUpdateDeliveryAgency(success=True)
