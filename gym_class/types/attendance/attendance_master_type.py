from graphene_django import DjangoObjectType

from gym_class.models import AttendanceMaster


class AttendanceMasterType(DjangoObjectType):
    class Meta:
        model = AttendanceMaster
