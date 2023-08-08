import graphene

from gym_student.models import AuditionMaster
from graphql_relay.node.node import from_global_id


class DeleteAuditionMaster(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, id):
        audition_master, audition_master_id = from_global_id(id)
        AuditionMaster.objects.get(pk=audition_master_id).delete()

        return DeleteAuditionMaster(success=True)