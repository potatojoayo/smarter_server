import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from base_classes import CountableConnectionBase
from gym_student.models import Student


class StudentNode(DjangoObjectType):
    class Meta:
        model = Student
        interfaces = (relay.Node,)
        connection_class = CountableConnectionBase
        filter_fields = {
            'class_master__name': ['exact'],
            'level__name': ['exact'],
            'school__name': ['icontains'],
            'name': ['icontains']
        }

    student_id = graphene.Int()

    @staticmethod
    def resolve_student_id(root, _):
        print(root.id)
        return root.id
