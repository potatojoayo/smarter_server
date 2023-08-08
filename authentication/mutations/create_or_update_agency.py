import graphene
from django.db import IntegrityError

from authentication.models import User
from business.models import Agency
from business.types.agency.agency_input_type import AgencyInputType
from django.contrib.auth.models import Group


class CreateOrUpdateAgency(graphene.Mutation):
    class Arguments:
        agency = AgencyInputType()

    success = graphene.Boolean()
    duplicated = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, agency):

        agency_user = agency.user
        if agency.id:
            User.objects.filter(pk=agency_user.id).update(**agency_user)
            user = User.objects.get(pk=agency_user.id)
            if agency_user.password:
                user.set_password(agency_user.password)
                user.save()
            agency.pop('user', None)
            Agency.objects.filter(user=user).update(**agency)
        else:
            try:
                new_agency_user = User.objects.create_user(**agency_user)
                group = Group.objects.get(name='체육사')
                new_agency_user.groups.add(group)
                agency.pop('user', None)
                Agency.objects.create(user=new_agency_user, **agency)
            except IntegrityError:
                return CreateOrUpdateAgency(success=False, duplicated=True)

        return CreateOrUpdateAgency(success=True, duplicated=False)

