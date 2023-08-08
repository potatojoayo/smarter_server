import graphene
from common.models import Membership


class UpdateMembership(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        condition = graphene.Int()
        threshold = graphene.Int()
        percentage = graphene.Float()
        max = graphene.Int()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, name, condition, threshold, percentage,
               max):
        Membership.objects.filter(name=name).update(condition=condition,
                                                    threshold=threshold,
                                                    percentage=percentage,
                                                    max=max)
        return UpdateMembership(success=True)
