from graphene_django import DjangoObjectType

from business.models import Agency


class AgencyType(DjangoObjectType):

    class Meta:
        model = Agency
        fields = '__all__'
