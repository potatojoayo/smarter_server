import graphene

from common.models import DeliveryAgency


class DeleteDeliveryAgency(graphene.Mutation):
    class Arguments:
        delivery_agency_id = graphene.Int()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, delivery_agency_id):
        DeliveryAgency.objects.filter(pk=delivery_agency_id).delete()

        return DeleteDeliveryAgency(success=True)