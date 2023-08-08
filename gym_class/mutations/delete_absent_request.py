import graphene

from gym_class.models import AbsentRequest


class DeleteAbsentRequest(graphene.Mutation):
    class Arguments:
        absent_request_id = graphene.Int()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, absent_request_id):
        absent_request = AbsentRequest.objects.get(pk=absent_request_id)
        absent_request.delete()

        return DeleteAbsentRequest(success=True)