import graphene
from django.db import IntegrityError

from authentication.models import User
from business.models import Subcontractor
from django.contrib.auth.models import Group

from business.types.subcontractor.subcontractor_input_type import SubcontractorInputType


class CreateOrUpdateSubcontractor(graphene.Mutation):
    class Arguments:
        subcontractor = SubcontractorInputType()

    success = graphene.Boolean()
    duplicated = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, subcontractor):

        user = subcontractor.user
        if user.id:
            User.objects.filter(pk=user.id).update(**user)
            user = User.objects.get(pk=user.id)
            if user.password:
                user.set_password(user.password)
                user.save()
            subcontractor.pop('user', None)
            Subcontractor.objects.filter(user=user).update(**subcontractor)
        else:
            try:
                new_agency_user = User.objects.create_user(**user)
                group = Group.objects.get(name='작업실')
                new_agency_user.groups.add(group)
                subcontractor.pop('user', None)
                Subcontractor.objects.create(user=new_agency_user, **subcontractor)
            except IntegrityError:
                return CreateOrUpdateSubcontractor(success=False, duplicated=True)

        return CreateOrUpdateSubcontractor(success=True, duplicated=False)

