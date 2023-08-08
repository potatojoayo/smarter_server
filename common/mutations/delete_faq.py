import graphene

from common.models import Faq


class DeleteFaq(graphene.Mutation):
    class Arguments:
        faq_id = graphene.Int()

    success = graphene.Int()

    @classmethod
    def mutate(cls, _, __, faq_id):
        Faq.objects.filter(pk=faq_id).delete()

        return DeleteFaq(success=True)
