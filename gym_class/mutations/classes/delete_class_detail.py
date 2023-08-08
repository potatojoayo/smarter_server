from django.utils import timezone

import graphene

from gym_class.models import ClassDetail


class DeleteClassDetail(graphene.Mutation):
    class Arguments:
        class_detail_id = graphene.Int()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, class_detail_id):
        class_detail = ClassDetail.objects.get(pk=class_detail_id)
        class_detail.is_deleted = True
        now = timezone.localtime()
        class_detail.date_deleted = now
        class_detail.save()
        return DeleteClassDetail(success=True)
