import graphene
from graphene_django import DjangoObjectType
from graphene import relay

from base_classes import CountableConnectionBase
from class_payment.models import ClassPaymentMaster


class ClassPaymentMasterNode(DjangoObjectType):
    class Meta:
        model = ClassPaymentMaster
        interfaces = (relay.Node,)
        filter_fields = {
            'class_master__name': ['exact'],
            'payment_status': ['exact'],
            'is_approved': ['exact'],
            'type': ['exact'],
        }
        connection_class = CountableConnectionBase

    class_payment_master_id = graphene.Int()

    @staticmethod
    def resolve_class_payment_master_id(root, _):
        return root.id
