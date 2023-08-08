import graphene
from graphene_django import DjangoObjectType
from gym_student.models import Student


class StudentType(DjangoObjectType):
    class Meta:
        model = Student

    student_id = graphene.Int()

    @staticmethod
    def resolve_student_id(root, _):
        return root.id