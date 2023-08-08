import os

import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from base_classes import CountableConnectionBase
from business.models import Agency


class AgencyNode(DjangoObjectType):
    class Meta:
        model = Agency
        interfaces = (relay.Node,)
        filter_fields = {
            'date_created': ['lte', 'gte'],
            'name':['icontains']
        }
        connection_class = CountableConnectionBase

    agency_id = graphene.Int()
    business_registration_certificate = graphene.String()

    @staticmethod
    def resolve_agency_id(root, _):
        return root.id

    @staticmethod
    def resolve_business_registration_certificate(root, _):
        if root.business_registration_certificate:
            return os.environ.get("BASE_URL")+root.business_registration_certificate.url
