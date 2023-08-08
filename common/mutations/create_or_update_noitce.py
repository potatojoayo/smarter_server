import graphene
from django.utils import timezone

from authentication.models import User
from common.models import Notice


class CreateOrUpdateNoice(graphene.Mutation):
    class Arguments:
        notice_id = graphene.Int()
        user_id = graphene.Int()
        title = graphene.String()
        contents = graphene.String()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, info, notice_id=None, user_id=None, title=None, contents=None):

        user = info.context.user

        if notice_id:
            Notice.objects.filter(pk=notice_id).update(user=user, title=title, contents=contents)
        else:
            Notice.objects.create(user=user, title=title, contents=contents, date_created=timezone.now())

        return CreateOrUpdateNoice(success=True)
