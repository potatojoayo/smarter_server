from graphene_django import DjangoObjectType
from order.models import EasyOrder



class EasyOrderType(DjangoObjectType):
    class Meta:
        model = EasyOrder


