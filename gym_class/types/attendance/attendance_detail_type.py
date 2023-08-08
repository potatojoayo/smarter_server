from graphene_django import DjangoObjectType

from gym_class.models import AttendanceDetail


class AttendanceDetailType(DjangoObjectType):
    class Meta:
        model = AttendanceDetail
