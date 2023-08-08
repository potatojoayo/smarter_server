import graphene
from django.utils import timezone
from gym_class.models import ClassMaster


class DeleteClassMaster(graphene.Mutation):
    class Arguments:
        class_master_ids = graphene.List(graphene.Int)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, class_master_ids):
        now = timezone.localtime()
        class_masters = ClassMaster.objects.filter(pk__in=class_master_ids)
        for class_master in class_masters:
            class_master.is_deleted = True
            class_master.date_deleted = now
            class_master.save()
            class_details = class_master.class_details.filter(is_deleted=False)
            for class_detail in class_details:
                class_detail.is_deleted = True
                class_detail.date_deleted = now
                class_detail.save()

        return DeleteClassMaster(success=True)
