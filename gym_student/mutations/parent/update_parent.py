import graphene

from authentication.models import User
from gym_student.models import Parent, Relationship
from gym_student.types.parent_input_type import ParentInputType


class UpdateParent(graphene.Mutation):
    class Arguments:
        parent_object = ParentInputType()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, info, parent_object):
        user = info.context.user
        user.phone = parent_object.phone
        user.name = parent_object.name
        user.save()
        parent = Parent.objects.get(user=user)
        relationship, created = Relationship.objects.get_or_create(name=parent_object.relationship_name)
        parent.relationship = relationship
        parent.zip_code = parent_object.zip_code
        parent.address = parent_object.address
        parent.detail_address = parent_object.detail_address
        parent.supporter_name = parent_object.supporter_name
        supporter_relationship, created = Relationship.objects.get_or_create(name=parent_object.supporter_relationship)
        parent.supporter_relationship = supporter_relationship
        parent.supporter_phone = parent_object.supporter_phone
        parent.save()

        return UpdateParent(success=True)
