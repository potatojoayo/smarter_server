import graphene

from gym_class.models import Level


class DeleteLevel(graphene.Mutation):
    class Arguments:
        delete_level_ids = graphene.List(graphene.Int)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, delete_level_ids):
        Level.objects.filter(pk__in=delete_level_ids).delete()

        return DeleteLevel(success=True)
