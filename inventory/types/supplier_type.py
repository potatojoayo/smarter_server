import os
import graphene
from graphene_django import DjangoObjectType

from inventory.models import Supplier


class SupplierType(DjangoObjectType):
    class Meta:
        model = Supplier
        filter_fields = {
            'id': ['exact']
        }

    business_registration_certificate = graphene.String()

    @staticmethod
    def resolve_business_registration_certificate(root, _):
        try:
            return os.environ.get("BASE_URL")+root.business_registration_certificate.url
        except:
            return None


