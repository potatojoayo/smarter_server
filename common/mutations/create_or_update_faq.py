import graphene

from authentication.models import User
from common.models import Faq


class CreateOrUpdateFaq(graphene.Mutation):
    class Arguments:
        faq_id = graphene.Int()
        title = graphene.String()
        contents = graphene.String()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, info, faq_id=None, title=None, contents=None):

        user = info.context.user

        if faq_id:
            Faq.objects.filter(pk=faq_id).update(user=user, title=title, contents=contents)
        else:
            Faq.objects.create(user=user, title=title, contents=contents)

        return CreateOrUpdateFaq(success=True)
